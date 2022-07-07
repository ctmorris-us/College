cc = gcc
JAVAC = javac
JRE = java
PAGER = less

.PHONY = clean run-py run-c read run-java test.out test-java 

cleanall : clean

clean :
	@echo ""
test-java : test.out expected.out
	-@if diff test.out expected.out &> /dev/null ; then \
  		echo "Passed!" ;\
	else \
  		echo "Not the same!" ;\
	fi	
test-out : foo.class
	$(JRE) foo > $@
run-java : foo.class
	$(JRE) foo
food.class : foo.java
	$(JAVAC) $<
read : README
	$(PAGER) README
run-py : foo.py
	python foo.py
run-c : foo
	./foo
foo: foo.o main.o
	$(cc) -o foo main.o foo.o
foo.o : foo.c foo.h
	$(cc) -c foo.c
main.o : main.c foo.h
	$(cc) -c main.c


