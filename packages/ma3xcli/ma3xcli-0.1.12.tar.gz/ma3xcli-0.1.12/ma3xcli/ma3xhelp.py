#!/usr/bin/env python
import os,sys

def main():
	print(os.system("ls -la"))

if __name__ == "__main__":
    typer.run(main)