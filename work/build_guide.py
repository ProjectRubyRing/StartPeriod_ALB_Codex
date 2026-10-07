"""Build consistent XLSX and Markdown artifacts without external application access."""
from __future__ import annotations

import json
import math
import re
from pathlib import Path
from functools import lru_cache
from datetime import datetime

import xlsxwriter
from PIL import ImageFont

import guide_content as g
import guide_examples as examples

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)
EXAMPLES = ROOT / "work" / "examples"
EXAMPLES.mkdir(exist_ok=True)
STEM = "ECS_Fargate_HealthCheck_Design_2026-10-07"
FONT = "Meiryo UI"
FONT_FILE = Path("C:/Windows/Fonts/meiryo.ttc")
SOURCE_MAP = {x[0]: x for x in g.SOURCES}
MODE_NAMES = {"parallel_all":"全並列", "serial":"直列", "parallel_adot":"ADOT後に並列", "start":"START", "wrapper":"JVM待機"}


@lru_cache(maxsize=None)
def font(size=11, bold=False):
    # Meiryo UI Regular/Bold is face 2 in these Windows font collections.
    path = FONT_FILE.with_name("meiryob.ttc") if bold else FONT_FILE
    return ImageFont.truetype(str(path), round(size*96/72), index=2)


def wrapped_lines(text, pixels, size=11, bold=False):
    """Conservative visual wrapping; account for CJK glyph width, not byte count."""
    f=font(size,bold)
    limit=max(25,pixels-16)
    lines=[]
    for raw in str(text).split('\n'):
        if not raw:
            lines.append('')
            continue
        chunk=''
        for ch in raw:
            if chunk and f.getlength(chunk+ch)>limit:
                lines.append(chunk)
                chunk=ch
            else:
                chunk+=ch
        lines.append(chunk)
    return lines


def row_height(text, pixels, size=11, bold=False, minimum=24):
    # Leave room for Excel's word-boundary wrapping and column-width rounding.
    count=len(wrapped_lines(text,pixels*0.94,size,bold))
    return min(405,max(minimum,count*17+12))


class Book:
    def __init__(self,path):
        self.wb=xlsxwriter.Workbook(path,{"strings_to_formulas":False,"strings_to_urls":False})
        self.wb.set_properties({"title":g.TITLE,"subject":g.SUBTITLE,"author":"Codex","comments":"仕様と仮定を区別した設計資料。AWSへの適用は行っていません。","created":datetime(2026,10,7)})
        self.wb.formats[0].set_font_name(FONT)
        self.wb.formats[0].set_font_size(11)
        self.wb.set_calc_mode('auto')
        self.cache={}
        self.sheets={}
        self.source_rows={}
        self.meta={"sheets":{},"calculator":{},"pattern_expectations":{z['id']:g.timing(z) for z in g.PATTERNS}}

    def fmt(self,kind='body',**extra):
        styles={
            'body':dict(font_color='#222222',bg_color='#FFFFFF',text_wrap=True,valign='top',border=1,border_color='#D5D5D5'),
            'alternate':dict(font_color='#222222',bg_color='#F1F1F1',text_wrap=True,valign='top',border=1,border_color='#D5D5D5'),
            'title':dict(font_size=21,bold=True,font_color='#FFFFFF',bg_color='#242424',valign='vcenter'),
            'subtitle':dict(font_size=10,font_color='#555555',text_wrap=True,valign='vcenter'),
            'section':dict(font_size=12,bold=True,font_color='#FFFFFF',bg_color='#555555',valign='vcenter',text_wrap=True),
            'head':dict(bold=True,font_color='#FFFFFF',bg_color='#363636',text_wrap=True,valign='vcenter',border=1,border_color='#FFFFFF'),
            'prose_label':dict(bold=True,font_color='#222222',bg_color='#E6E6E6',text_wrap=True,valign='top',border=1,border_color='#CCCCCC'),
            'code':dict(font_size=10,font_color='#202020',bg_color='#F2F2F2',text_wrap=True,valign='top'),
            'link':dict(font_size=10,font_color='#333333',underline=True,valign='vcenter'),
            'ref':dict(font_size=9,font_color='#555555',text_wrap=True,valign='vcenter'),
            'input':dict(bg_color='#FFFFFF',font_color='#111111',border=2,border_color='#777777',text_wrap=True,valign='vcenter',num_format='0.0;[Black]-0.0;0'),
            'formula':dict(bg_color='#E3E3E3',font_color='#111111',bold=True,border=1,border_color='#AAAAAA',text_wrap=True,valign='vcenter',num_format='0.0;[Black]-0.0;0'),
            'gantt':dict(bg_color='#777777',font_color='#FFFFFF',align='center',valign='vcenter',border=1,border_color='#FFFFFF',font_size=9),
            'empty':dict(bg_color='#FAFAFA',border=1,border_color='#E0E0E0'),
        }
        d=dict(font_name=FONT,font_size=11)
        d.update(styles[kind]);d.update(extra)
        key=tuple(sorted(d.items()))
        if key not in self.cache:self.cache[key]=self.wb.add_format(d)
        return self.cache[key]

    def new(self,name,title,intro,widths=None):
        ws=self.wb.add_worksheet(name)
        if widths is None: widths=[3.3]*48
        widths=list(widths)
        self.sheets[name]=(ws,widths)
        for i,width in enumerate(widths):ws.set_column(i,i,width)
        ws.hide_gridlines(2)
        ws.set_zoom(85 if len(widths)>12 else 90)
        ws.set_tab_color('#777777')
        ws.set_landscape();ws.set_paper(8)  # A3 landscape
        ws.fit_to_pages(1,0)
        ws.set_margins(0.25,0.25,0.35,0.35)
        ws.set_header('&L&"Meiryo UI,Regular"&9ECS Fargate 設計ガイド&R2026-10-07')
        ws.set_footer('&L&"Meiryo UI,Regular"&8仮定の値は実測で置換&R&P / &N')
        ws.repeat_rows(0,3)
        self.merge(ws,0,0,len(widths)-1,title,self.fmt('title'))
        ws.set_row(0,40)
        self.merge(ws,1,0,len(widths)-1,g.SUBTITLE,self.fmt('subtitle'))
        ws.set_row(1,25)
        self.merge(ws,2,0,len(widths)-1,intro,self.fmt('subtitle'))
        ws.set_row(2,row_height(intro,self.pixels(widths),10,minimum=32))
        navcol=max(1,len(widths)//2)
        self.merge(ws,3,0,navcol-1,'',self.fmt('link'))
        self.merge(ws,3,navcol,len(widths)-1,'',self.fmt('link'))
        ws.write_url(3,0,"internal:'00_結論と読み方'!A1",self.fmt('link'),'目次へ')
        ws.write_url(3,navcol,"internal:'18_出典と適用範囲'!A1",self.fmt('link'),'出典一覧へ')
        ws.set_row(3,22);ws.set_row(4,8)
        ws.freeze_panes(5,0)
        return ws,widths,5

    @staticmethod
    def pixels(widths):
        return sum(w*7+5 for w in widths)

    @staticmethod
    def merge(ws,r,a,b,text,fmt):
        if a==b:
            if isinstance(text,(float,int)):ws.write_number(r,a,text,fmt)
            else:ws.write_string(r,a,str(text),fmt)
        else:ws.merge_range(r,a,r,b,text,fmt)

    def spans(self,widths,desired):
        n=len(widths);k=len(desired)
        if n==k:return [(i,i) for i in range(n)]
        cumulative=0;spans=[];start=0
        for i,v in enumerate(desired):
            cumulative+=v
            end=n-1 if i==k-1 else max(start,min(n-(k-i),round(cumulative/sum(desired)*n)-1))
            spans.append((start,end));start=end+1
        return spans

    def heading(self,ws,widths,r,title):
        self.merge(ws,r,0,len(widths)-1,title,self.fmt('section'))
        ws.set_row(r,29)
        return r+1

    def refs(self,ws,widths,r,refs):
        if not refs:return r
        text='出典：'+' / '.join(refs.split())+'（18_出典と適用範囲の同IDを参照）'
        self.merge(ws,r,0,len(widths)-1,text,self.fmt('ref'))
        ws.set_row(r,21)
        return r+1

    def prose(self,ws,widths,r,block):
        if len(widths)>12: split=10
        else:split=1
        lp=self.pixels(widths[:split]);rp=self.pixels(widths[split:])
        h=max(row_height(block['heading'],lp,bold=True),row_height(block['text'],rp))
        self.merge(ws,r,0,split-1,block['heading'],self.fmt('prose_label'))
        self.merge(ws,r,split,len(widths)-1,block['text'],self.fmt('body'))
        ws.set_row(r,h)
        r=self.refs(ws,widths,r+1,block.get('refs',''))
        ws.set_row(r,8)
        return r+1

    def table(self,ws,widths,r,block,filter_table=False):
        r=self.heading(ws,widths,r,block['heading'])
        desired=block['widths'] or [1]*len(block['headers'])
        spans=self.spans(widths,desired)
        start=r
        header_h=30
        for text,(a,b) in zip(block['headers'],spans):
            self.merge(ws,r,a,b,text,self.fmt('head'))
            header_h=max(header_h,row_height(text,self.pixels(widths[a:b+1]),bold=True))
        ws.set_row(r,header_h);r+=1
        for idx,row in enumerate(block['rows']):
            height=25
            for value,(a,b) in zip(row,spans):
                fmt=self.fmt('alternate' if idx%2 else 'body')
                if isinstance(value,(int,float)):fmt=self.fmt('alternate' if idx%2 else 'body',align='center',valign='vcenter',num_format='0')
                self.merge(ws,r,a,b,value,fmt)
                height=max(height,row_height(value,self.pixels(widths[a:b+1])))
                if str(value).startswith('https://') and a!=b:
                    ws.write_url(r,a,value,fmt,value)
                if str(value).startswith('https://') and a==b:
                    ws.write_url(r,a,value,fmt,value)
            if ws.name=='18_出典と適用範囲':self.source_rows[row[0]]=r
            ws.set_row(r,height);r+=1
        if filter_table and all(a==b for a,b in spans):
            ws.autofilter(start,0,r-1,len(widths)-1)
            ws.freeze_panes(start+1,2 if ws.name=='05_コンテナ設定' else 1)
        r=self.refs(ws,widths,r,block.get('refs',''))
        ws.set_row(r,10)
        return r+1

    def code(self,ws,widths,r,block):
        r=self.heading(ws,widths,r,block['heading']+'  ['+block['language']+']')
        for line in block['text'].splitlines():
            self.merge(ws,r,0,len(widths)-1,line or ' ',self.fmt('code'))
            ws.set_row(r,max(19,len(wrapped_lines(line,self.pixels(widths),10))*14+4))
            r+=1
        r=self.refs(ws,widths,r,block.get('refs',''))
        ws.set_row(r,9)
        return r+1

    def finish_sheet(self,ws,widths,r):
        ws.print_area(0,0,max(0,r-1),len(widths)-1)
        self.meta['sheets'][ws.name]={"rows":r,"columns":len(widths),"widths":widths}

    def render_section(self,s):
        flat=s['sheet'] in ['05_コンテナ設定','07_起動時系列','08_時間計算']
        widths=([40,20,10,90] if s['sheet']=='08_時間計算' else next(b['widths'] for b in s['blocks'] if b['type']=='table') if flat else None)
        ws,widths,r=self.new(s['sheet'],s['title'],s['intro'],widths)
        if s['sheet']=='00_結論と読み方':
            r=self.heading(ws,widths,r,'目次：クリックして移動')
            contents=list(g.SECTIONS)
            visual_index=next(i+1 for i,item in enumerate(contents) if item['sheet']=='07_起動時系列')
            contents.insert(visual_index,{'sheet':'07b_時系列図','title':'P2 / P4 / P3の比較図'})
            for idx,item in enumerate(contents):
                col=0 if idx%2==0 else 24
                rr=r+idx//2
                self.merge(ws,rr,col,col+23,'',self.fmt('body'))
                ws.write_url(rr,col,f"internal:'{item['sheet']}'!A1",self.fmt('link'),item['sheet']+'  '+item['title'])
                ws.set_row(rr,25)
            r+=math.ceil(len(contents)/2)+1
        for b in s['blocks']:
            if b['type']=='prose':r=self.prose(ws,widths,r,b)
            elif b['type']=='code':r=self.code(ws,widths,r,b)
            else:r=self.table(ws,widths,r,b,filter_table=flat and s['sheet']!='08_時間計算')
        if s['sheet']=='08_時間計算':r=self.calculator(ws,widths,r)
        self.finish_sheet(ws,widths,r)

    def calculator(self,ws,widths,r):
        r=self.heading(ws,widths,r,'入力できる計算表：白いB列を変更 / 灰色B列は計算結果')
        self.merge(ws,r,0,3,'P4を初期値とします。直列へ切り替えるとバック120秒の成立条件も判定します。startPeriodは準備時間の式に足しません。',self.fmt('subtitle'))
        ws.set_row(r,36);r+=1
        inputs=[
            ('mode','構成モード','ADOT後に並列','選択','全並列 / ADOT後に並列 / 直列 / START / JVM待機'),
            ('a','ADOT実準備 A',20,'秒','ADOTコンテナ開始から実際の準備完了まで。'),
            ('b','バック実準備 B',200,'秒','バックコンテナ開始からAPIが使えるまで。'),
            ('f','フロント実準備 F',200,'秒','フロントJVM開始からフロント自体が準備完了するまで。'),
            ('da','ADOT検知余裕 dA',5,'秒','検査位相・実行・通知の遅れを含む入力。'),
            ('db','バック検知余裕 dB',10,'秒','実測値に置き換える。'),
            ('df','フロント検知余裕 dF',10,'秒','実測値に置き換える。'),
            ('gap','START遅れ / JVM待ち確認遅れ',5,'秒','STARTはコンテナ開始までの遅れ。JVM待機は準備完了を拾う遅れ。'),
            ('ts','task.startedAtの相対時刻 Ts',25,'秒','起点t=0からの値を実測する。モード変更時は必ず確認。'),
            ('i','ALB interval I',10,'秒','指定可能5–300。'),
            ('h','ALB復帰成功回数 H',2,'回','指定可能2–10。新規登録の初回成功1回とは区別。'),
            ('tau','ALB応答等の余裕 τ',2,'秒','AWSの最大値保証ではない。伝播遅延も必要に応じMに含める。'),
            ('m','追加の設計余裕 M',60,'秒','起動のばらつき・管理系の通知遅れなど。'),
            ('g','採用候補G',300,'秒','ECSサービスのhealthCheckGracePeriodSeconds。'),
            ('ast','ADOT startTimeout',120,'秒','ADOTのHEALTHYを待つ場合。Fargate上限120。'),
            ('bst','バック startTimeout',120,'秒','直列モードだけでHEALTHY依存の成立条件に使う。'),
        ]
        cells={};iv={}
        for key,label,value,unit,note in inputs:
            for col,val in [(0,label),(2,unit),(3,note)]:ws.write(r,col,val,self.fmt('alternate'))
            ws.write(r,1,value,self.fmt('input'))
            ws.set_row(r,max(34,row_height(note,self.pixels([widths[3]]))))
            cell=f'B{r+1}';cells[key]=cell;iv[cell]=value
            if key=='mode':ws.data_validation(r,1,r,1,{'validate':'list','source':list(MODE_NAMES.values()),'input_title':'構成モード','input_message':'時間の足し方を切り替えます。','error_title':'リストから選択','error_message':'有効な構成モードを選んでください。'})
            else:
                bounds={'i':(5,300),'h':(2,10),'ast':(2,120),'bst':(2,120),'g':(0,2147483647)}.get(key,(0,1000000))
                ws.data_validation(r,1,r,1,{'validate':'integer' if key in ['i','h','ast','bst','g'] else 'decimal','criteria':'between','minimum':bounds[0],'maximum':bounds[1],'error_type':'stop','error_title':'入力範囲を確認','error_message':f'{bounds[0]}〜{bounds[1]}を入力してください。'})
            r+=1
        r+=1;r=self.heading(ws,widths,r,'計算結果（入力した仮定が正しい場合）')
        results=[]
        def calc(key,label,formula,value,note):
            nonlocal r
            c=f'B{r+1}'
            ws.write(r,0,label,self.fmt('alternate'))
            ws.write_formula(r,1,formula,self.fmt('formula'),value)
            ws.write(r,2,'秒' if isinstance(value,(int,float)) else '判定',self.fmt('alternate'))
            ws.write(r,3,note,self.fmt('body'))
            ws.set_row(r,max(38,row_height(note,self.pixels([widths[3]])),row_height(value,self.pixels([widths[1]]))))
            cells[key]=c;results.append({'key':key,'cell':c,'formula':formula,'cached':value});r+=1
        calc('ha','ADOT初回HEALTHY HA',f'={cells["a"]}+{cells["da"]}',25,'startPeriodではなく、実準備時間＋検知余裕。')
        calc('hb','バック初回HEALTHY HB',f'={cells["b"]}+{cells["db"]}',210,'バック自身の開始から数える。直列なら120秒との比較が重要。')
        calc('hf','フロント初回HEALTHY HF',f'={cells["f"]}+{cells["df"]}',210,'JVM開始から数える。ラッパー待機分は別に加算。')
        calc('bs','バック開始時刻',f'=IF({cells["mode"]}="全並列",0,{cells["ha"]})',25,'最初のコンテナ開始をt=0とする。')
        calc('fs','フロントコンテナ開始',f'=IF({cells["mode"]}="直列",{cells["bs"]}+{cells["hb"]},IF({cells["mode"]}="START",{cells["bs"]}+{cells["gap"]},{cells["bs"]}))',25,'依存期限超過時は、この値に到達しない。下の判定を先に確認する。')
        calc('jvm','フロントJVM開始',f'=IF({cells["mode"]}="JVM待機",{cells["bs"]}+{cells["b"]}+{cells["gap"]},{cells["fs"]})',25,'JVM待機だけはコンテナが開始した後に待つ。')
        calc('ready','ALB用readiness成立',f'=MAX({cells["bs"]}+{cells["b"]},{cells["jvm"]}+{cells["f"]})',225,'フロントとバックの双方が実際に利用可能な時刻。')
        calc('alb','ALB復帰見積もり',f'={cells["ready"]}+{cells["i"]}*{cells["h"]}+{cells["tau"]}',247,'復帰の連続成功回数を使う。初回成功だけならより早い場合がある。')
        calc('end','全体の健康確認時刻',f'=MAX({cells["ha"]},{cells["bs"]}+{cells["hb"]},{cells["jvm"]}+{cells["hf"]},{cells["alb"]})',247,'必須コンテナとALBの遅い方。CloudWatch Agentは非必須・依存なし。')
        calc('need','必要猶予の見積もり',f'=MAX(0,{cells["end"]}-{cells["ts"]})+{cells["m"]}',282,'ECS内部の厳密な実行期限ではない。ログ・イベントで実証する。')
        calc('rounded','30秒単位の切り上げ候補',f'=ROUNDUP({cells["need"]}/30,0)*30',300,'使いやすい整数へ丸めた候補。AWS公式の推奨値ではない。')
        calc('ac','ADOT依存の判定',f'=IF({cells["mode"]}="全並列","依存なし",IF({cells["ha"]}<{cells["ast"]},"時間内","期限不足"))','時間内','期限と同時では余裕なしとして期限不足にする。')
        calc('bc','バックHEALTHY依存の判定',f'=IF({cells["mode"]}="直列",IF({cells["hb"]}<{cells["bst"]},"時間内","期限不足"),"依存なし")','依存なし','STARTをHEALTHY待ちと誤解しない。')
        calc('overall','総合判定',f'=IF(OR({cells["ac"]}="期限不足",{cells["bc"]}="期限不足"),"依存構成の見直し",IF({cells["g"]}>={cells["need"]},"仮定上は猶予内","猶予不足"))','仮定上は猶予内','依存構成が不成立なら、猶予の計算より先に依存を見直す。')
        self.meta['calculator']={'sheet':ws.name,'cells':cells,'inputs':iv,'results':results}
        return r+1

    def gantt(self):
        widths=[36]+[6.3]*22
        ws,widths,r=self.new('07b_時系列図','P2とP4の起動を図で比較','1目盛り20秒。棒の区切りは概略、行見出しの数値と07_起動時系列の値が基準です。灰色の濃さで待機・初期化・準備完了を区別します。',widths)
        for pid in ['P2','P4','P3']:
            z=next(p for p in g.PATTERNS if p['id']==pid);t=g.timing(z)
            r=self.heading(ws,widths,r,pid+'  '+z['name'])
            ws.write(r,0,'最初のコンテナ開始から',self.fmt('head'))
            for i in range(22):ws.write(r,i+1,i*20,self.fmt('head',align='center',font_size=9))
            ws.set_row(r,34);r+=1
            if pid=='P3':
                bands=[('ADOT（停止処理は未描画）',0,25,'healthy_until_failure'),('バック',25,145,'timeout'),('フロント（未起動）',0,0,'not_started')]
            else:
                bands=[('ADOT',0,t['ah'],'healthy'),('バック',t['bs'],t['bh'],'healthy'),('フロント',t['fs'],t['fh'],'healthy'),('ALB復帰まで',0,t['alb'],'alb'),('ECS猶予',z['task'],z['task']+z['grace'],'grace')]
            for label,start,end,kind in bands:
                ws.write(r,0,f'{label}\n{start} → {end} 秒' if kind!='not_started' else label,self.fmt('prose_label'))
                for i in range(22):
                    moment=i*20
                    if kind=='not_started' or (kind=='healthy_until_failure' and moment>=145):color='#FAFAFA'
                    elif moment<start:color='#E6E6E6'
                    elif moment<end:color='#777777' if kind!='grace' else '#B6B6B6'
                    else:color='#333333' if kind in ('healthy','healthy_until_failure') else '#FAFAFA'
                    ws.write_blank(r,i+1,None,self.fmt('empty',bg_color=color))
                ws.set_row(r,39);r+=1
            note=('バックの想定初回HEALTHYはt=235。依存期限はt=145付近なので、フロント開始へ進めない。' if pid=='P3' else f'全体健康確認 t={t["end"]}。task.startedAt=t={z["task"]}の仮定では、G={z["grace"]}の期限はt={z["task"]+z["grace"]}。')
            self.merge(ws,r,0,len(widths)-1,note,self.fmt('body'));ws.set_row(r,34);r+=2
        self.merge(ws,r,0,len(widths)-1,'濃灰：コンテナ健康確認済み / 中灰：初期化・健康確認待ち / 淡灰：依存待ちまたはECS猶予。ALBの帯は計算上の復帰までの時間で、実際の検査開始時刻を表しません。',self.fmt('subtitle'))
        ws.set_row(r,40);r+=1
        self.finish_sheet(ws,widths,r)


def source_links(refs):
    return ' '.join(f'[{sid} {SOURCE_MAP[sid][1]}]({SOURCE_MAP[sid][2]})' for sid in refs.split())


def markdown():
    parts=[f'# {g.TITLE}',g.SUBTITLE,f'確認日：{g.DATE}。Excel版と共通の原稿から生成。実起動時間は仮定です。','## 目次']
    for s in g.SECTIONS:parts.append(f'- [{s["sheet"]} {s["title"]}](#{s["sheet"]})')
    parts.append('')
    for s in g.SECTIONS:
        parts.extend([f'<a id="{s["sheet"]}"></a>',f'## {s["sheet"]}｜{s["title"]}',s['intro']])
        for b in s['blocks']:
            parts.append(f'### {b["heading"]}')
            if b['type']=='prose':parts.append(b['text'])
            elif b['type']=='code':parts.append(f'```{b["language"]}\n{b["text"]}\n```')
            else:
                def cell(v):return str(v).replace('|','\\|').replace('\n','<br>')
                lines=['| '+' | '.join(map(cell,b['headers']))+' |','| '+' | '.join(['---']*len(b['headers']))+' |']
                for row in b['rows']:
                    values=[]
                    for v in row:
                        if str(v).startswith('https://'):values.append(f'[公式資料を開く]({v})')
                        else:values.append(cell(v))
                    lines.append('| '+' | '.join(values)+' |')
                parts.append('\n'.join(lines))
            if b.get('refs'):parts.append('出典：'+source_links(b['refs']))
        if s['sheet']=='07_起動時系列':
            parts.extend(['### 依存関係の図',r'''```mermaid
flowchart LR
  A[ADOT準備完了] -->|HEALTHY| B[バックEAP開始]
  B -->|HEALTHY: 120秒以内に成立| F[フロントEAP開始]
  C[CloudWatch Agent] --- I[独立して開始]
```''','P4ではADOTからバック・フロントへそれぞれHEALTHY依存を置き、バックとフロントのHEALTHY依存を外します。'])
        if s['sheet']=='08_時間計算':
            parts.append('### Excel計算表の初期値と使い方')
            parts.append('構成モード=ADOT後に並列、A=20、B=200、F=200、dA=5、dB=10、dF=10、Ts=25、ALB I=10・H=2・τ=2、M=60、候補G=300。全体の健康確認はt=247、必要猶予は247−25＋60=282、30秒単位の切り上げは300です。')
            parts.append('Excelの白い入力セルを編集してください。直列へ変えるとHB=210がstartTimeout=120を超えるため「依存構成の見直し」と表示します。各入力欄に型と範囲の検証を設定しています。計算セルは灰色です。モードを変えたらTsも実測に合わせます。')
    return '\n\n'.join(parts)+'\n'


def main():
    for z in g.PATTERNS:
        (EXAMPLES/f'{z["id"]}_container_definitions.json').write_text(json.dumps(examples.containers(z),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (EXAMPLES/'P4_task_definition.json').write_text(json.dumps(examples.TASK,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (EXAMPLES/'main.tf').write_text(examples.TERRAFORM.strip()+'\n',encoding='utf-8')
    (EXAMPLES/'proc-healthcheck.go').write_text(examples.GO_PROBE.strip()+'\n',encoding='utf-8')
    book=Book(OUT/(STEM+'.xlsx'))
    for s in g.SECTIONS:
        book.render_section(s)
        if s['sheet']=='07_起動時系列':book.gantt()
    book.wb.close()
    (OUT/(STEM+'.md')).write_text(markdown(),encoding='utf-8')
    (ROOT/'work'/'build_manifest.json').write_text(json.dumps(book.meta,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'xlsx':str(OUT/(STEM+'.xlsx')),'md':str(OUT/(STEM+'.md')),'sheets':len(book.meta['sheets']),'sources':len(g.SOURCES),'markdown_characters':len(markdown())},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
