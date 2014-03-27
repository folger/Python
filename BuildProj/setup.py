from cx_Freeze import setup, Executable

setup(
  name = "BuildProj",
  version = "0.1",
  description = "Build Origin Projects",
  executables = [Executable("BuildProj.pyw")]
)



