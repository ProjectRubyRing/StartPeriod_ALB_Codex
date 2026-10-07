// proc-healthcheck: inspect an exact executable path in this container's /proc.
package main

import (
    "fmt"
    "os"
    "path/filepath"
    "strconv"
)

func main() {
    if len(os.Args) != 2 || !filepath.IsAbs(os.Args[1]) {
        fmt.Fprintln(os.Stderr, "usage: proc-healthcheck /absolute/executable")
        os.Exit(2)
    }
    entries, err := os.ReadDir("/proc")
    if err != nil {
        fmt.Fprintln(os.Stderr, "cannot inspect /proc")
        os.Exit(1)
    }
    for _, entry := range entries {
        if !entry.IsDir() {
            continue
        }
        if _, err := strconv.Atoi(entry.Name()); err != nil {
            continue
        }
        exe, err := os.Readlink(filepath.Join("/proc", entry.Name(), "exe"))
        if err == nil && exe == os.Args[1] {
            os.Exit(0)
        }
    }
    fmt.Fprintln(os.Stderr, "expected process not found or not inspectable")
    os.Exit(1)
}
