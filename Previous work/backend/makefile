CXXFLAGS = -lstdc++ -Wall -std=c++17 #-fsanitize=address
ifneq ($(OS),Windows_NT)
	UNAME_S = $(shell uname -s)
	ifeq ($(UNAME_S),Darwin)
        CXXFLAGS += -undefined dynamic_lookup
    endif
endif

CPPFOLDER = SOMCpp

PYEXT = $(shell python3-config --extension-suffix)
PYPACKNAME = SOMCpp

SRCDIR = $(CPPFOLDER)/src
SRCS = MapRect.cpp MapHex.cpp Map2d.cpp Node.cpp SOM.cpp DeepSOM.cpp LVQ.cpp Evaluation.cpp
OBJS = $(SRCS:.cpp=.o)
EXE = $(PYPACKNAME)$(PYEXT)
INCLUDEDIR = $(SRCDIR)

DBGDIR = $(CPPFOLDER)/debug
DBGOBJS = $(addprefix $(DBGDIR)/, $(OBJS))
DBGCXXFLAGS = -g -DDEBUG -fsanitize=address -fPIC
DBGEXE = $(DBGDIR)/$(EXE)

RELDIR = $(CPPFOLDER)/release
RELOBJS = $(addprefix $(RELDIR)/, $(OBJS))
RELCXXFLAGS = -O3 -DNDEBUG -fPIC -ffast-math -funsafe-math-optimizations #-march=native
RELEXE = $(RELDIR)/$(EXE)

TESTSRCDIR = $(CPPFOLDER)/test
TESTOUTDIR = $(CPPFOLDER)/test_out
TESTOBJS = $(addprefix $(TESTOUTDIR)/, $(OBJS))
TESTOUTS = $(addprefix $(TESTOUTDIR)/, test_map2d.out test_node.out test_som.out test_mapRect.out test_mapHex.out test_deepSOM.out test_lvq.out)
TESTCXXFLAGS = -g -DDEBUG -fprofile-arcs -ftest-coverage -include $(TESTSRCDIR)/SOM_defines.hpp
TESTCOVERAGEDIR = $(TESTOUTDIR)/coverage


.PHONY: all clean debug prep release remake run_tests docs
.PRECIOUS: $(DBGOBJS) $(RELOBJS) $(TESTOBJS)


all: prep release debug test

debug: $(DBGEXE) $(DBGDIR)/__init__.py

$(DBGEXE): $(SRCDIR)/binder.cpp $(DBGOBJS)
	$(CXX) $(CXXFLAGS) $(DBGCXXFLAGS) -I$(INCLUDEDIR) -shared `python3 -m pybind11 --includes` -o $(DBGEXE) $^

$(DBGDIR)/%.o: $(SRCDIR)/%.cpp
	$(CXX) -c $(CXXFLAGS) $(DBGCXXFLAGS) -I$(INCLUDEDIR) -o $@ $<

$(DBGDIR)/__init__.py:
	echo from .$(PYPACKNAME) import \* > $(DBGDIR)/__init__.py

release: $(RELEXE) $(RELDIR)/__init__.py

$(RELEXE): $(SRCDIR)/binder.cpp $(RELOBJS)
	$(CXX) $(CXXFLAGS) $(RELCXXFLAGS) -I$(INCLUDEDIR) -shared `python3 -m pybind11 --includes` -o $(RELEXE) $^

$(RELDIR)/%.o: $(SRCDIR)/%.cpp
	$(CXX) -c $(CXXFLAGS) $(RELCXXFLAGS) -I$(INCLUDEDIR) -o $@ $<

$(RELDIR)/__init__.py:
	echo from .$(PYPACKNAME) import \* > $(RELDIR)/__init__.py


# To run tests and coverage, make prep -> make test -> make run_tests -> make lcov, check test_out/out/index.html
test: $(TESTOUTS) 

$(TESTOUTDIR)/%.out: $(TESTSRCDIR)/%.cpp $(TESTOBJS) $(TESTOUTDIR)/CatchMain.o 
	$(CXX) -I$(INCLUDEDIR) $(CXXFLAGS) $(TESTCXXFLAGS) $(TESTOBJS) $(TESTOUTDIR)/CatchMain.o -o $@ $< 

$(TESTOUTDIR)/CatchMain.o: $(TESTSRCDIR)/CatchMain.cpp
	$(CXX) -c -I$(INCLUDEDIR) $(CXXFLAGS) $(TESTCXXFLAGS) -o $@ $(TESTSRCDIR)/CatchMain.cpp

$(TESTOUTDIR)/%.o: $(SRCDIR)/%.cpp
	$(CXX) -c -I$(INCLUDEDIR) $(CXXFLAGS) $(TESTCXXFLAGS) -o $@ $<

run_tests: 
	for x in $(TESTOUTDIR)/*.out; do ./$$x -r compact; done

docs:
	doxygen SOMCpp/Doxyfile

prep:
	@mkdir -p $(DBGDIR) $(RELDIR) $(TESTOUTDIR) $(TESTCOVERAGEDIR)

remake: clean all

clean: clean_tests
	rm -f $(RELOBJS) $(RELEXE) $(DBGOBJS) $(DBGEXE) $(TESTOUTS) $(TESTOBJS) $(TESTOUTDIR)/CatchMain.o

clean_tests:
	find . -name "*.gcda" -type f -delete
	find . -name "*.gcno" -type f -delete
	find . -name "*.info" -type f -delete
	find . -name "*.dSYM" -type d -exec rm -r "{}" +

lcov:
	lcov --capture --directory $(TESTOUTDIR) --output-file $(TESTOUTDIR)/main_coverage.info
	lcov --remove $(TESTOUTDIR)/main_coverage.info *\.h -o $(TESTOUTDIR)/main_coverage.info
	lcov --remove $(TESTOUTDIR)/main_coverage.info *\.hpp -o $(TESTOUTDIR)/main_coverage.info
	lcov --remove $(TESTOUTDIR)/main_coverage.info *v1* -o $(TESTOUTDIR)/main_coverage.info
	lcov --remove $(TESTOUTDIR)/main_coverage.info *DeepSOM* -o $(TESTOUTDIR)/main_coverage.info
	lcov --remove $(TESTOUTDIR)/main_coverage.info *Evaluation* -o $(TESTOUTDIR)/main_coverage.info
	genhtml $(TESTOUTDIR)/main_coverage.info --output-directory $(TESTOUTDIR)/out