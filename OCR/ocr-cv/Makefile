CXX = g++
CXXFLAGS =	-O2 -g -Wall -fmessage-length=0

INCS = -I/usr/local/include
LIBS =
OCR_OBJS = ocr-cv.o
TESS_OBJS = TesseractTester.o

ocr:	$(OCR_OBJS)
	$(CXX) -o ocr $(OCR_OBJS) $(LIBS) $(INCS)

tess: $(TESS_OBJS)
	$(CXX) -o tess $(TESS_OBJS) $(LIBS) $(INCS) 

all:	ocr tess

clean:
	rm -f *.o tess ocr
