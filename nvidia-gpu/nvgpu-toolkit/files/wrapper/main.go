package main

import (
	"os"
	"syscall"
)

const (
	realBin    = "/usr/local/bin/nvidia-container-runtime.real"
	configEnv  = "NVIDIA_CTK_CONFIG_FILE_PATH"
	configPath = "/usr/local/etc/nvidia-container-runtime/config.toml"
)

func main() {
	// Set config path so the runtime finds config.toml under /usr/local/etc/.
	// containerd sanitizes the environment before forking OCI runtime subprocesses,
	// so machine.env values are not inherited — this wrapper injects it explicitly.
	os.Setenv(configEnv, configPath)

	if err := syscall.Exec(realBin, append([]string{realBin}, os.Args[1:]...), os.Environ()); err != nil {
		os.Exit(1)
	}
}
