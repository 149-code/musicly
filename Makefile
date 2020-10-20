all:
	pyinstaller musicly.py --onefile
clean:
	rm -rf build dist __pycache__ musicly.spec
