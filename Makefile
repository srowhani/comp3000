build:
	swig -python -o lib/modules/proccoli_wrap.c lib/modules/proccoli.i
	mv lib/modules/proccoli.py lib/
	sed -i -e 's/Python.h/python2.7\/Python.h/' lib/modules/proccoli_wrap.c
	gcc -fPIC -c lib/modules/proccoli.c lib/modules/proccoli_wrap.c -I/usr/local/include/python2.7
	gcc -shared proccoli.o proccoli_wrap.o -o lib/_proccoli.so
	make clean
clean:
	rm lib/modules/proccoli_wrap.c
	rm proccoli_wrap.o
	rm proccoli.o
