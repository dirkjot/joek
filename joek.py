# JoeK: Will obfuscate, joeify and otherwise entertain you with customized Java source
# Dirk P. Janssen, fall 2015


import sh
import re
import collections
import fileinput

withinmapping = {
  'Controller': 'Conjoer',
  'Tranformer': 'Trevormer',
  'Directive': 'Dirketive',
  'Service': 'Sergeorge',
  'Test': 'Rami',
  'Autowired': 'Autorami',
  'Inject': 'Inrami',
}

keywords = """
abstract	continue	for	new	switch
assert	default	goto	package	synchronized
boolean	do	if	private	this
break	double	implements	protected	throw
byte	else	import	public	throws
case	enum	instanceof	return	transient
catch	extends	int	short	try
char	final	interface	static	void
class	finally	long	strictfp	volatile
const	float	native	super	while
const  goto   true false  null  
Map List Array ArrayList Boolean Void
""".split()

dynamicmapping = {}

# find . -type f -name "*java" -exec cat {} \+ > tt
def mostfrequent(infilename="tt"):
    freq = {}
    with open(infilename, "r") as inf:
        for line in inf:
            line = spaceparens.sub(" ", line)
            for word in line.split():
                freq[word] = freq.setdefault('word',0) + 1
    freqkeys = collections.Counter(freq)
    freqkeys.most_common(100)
    

example = """
    @ManagedAttribute
    public int getCallCount() {
        return callCount;
    }

    @ManagedAttribute
    public long getCallTime() {
        if (this.callCount > 0)
            return this.accumulatedCallTime / this.callCount;
        else
            return 0;
    }

    public countService = 4;
    public countController = 5;
    public countDirective = 4;
    public countTransformer = 4;
    public countTest = 5;


    @Around("within(@org.springframework.stereotype.Repository *)")
    public Object invoke(ProceedingJoinPoint joinPoint) throws Throwable {
        if (this.enabled) {
            StopWatch sw = new StopWatch(joinPoint.toShortString());

            sw.start("invoke");
            try {
                return joinPoint.proceed();
            } finally {
                sw.stop();
                synchronized (this) {
                    this.callCount++;
                    this.accumulatedCallTime += sw.getTotalTimeMillis();
                }
            }
        } else {
            return joinPoint.proceed();
        }
    }

    public something Class OneTwo {  blooh } 
    public something Class OneTwoThree {  
       void OneTwoThree() { constructor }; 
    }
    public something Class OneTwoFour {  OneTwo.constructor() }
"""


spaceparens = re.compile('[](){}.,;/+=*:?[-]')
iscamel = re.compile('^[a-z]+[A-Z_]')
inwordboundary = re.compile('(?=[A-Z])')
classmatch = re.compile("Class\W+([A-Z_]+[a-zA-Z0-9_]+)\W+{")

def joewordTest():
    assert joeword("aTwo") == "aTwoJoe"
    assert joeword("aTwoThree") == "aTwoThreeJoe"
    assert joeword("aTwoThreeFour") == "aTwoThreeJoeFourJoe"
    assert joeword("aTwoThreeFourFive") == "aTwoThreeJoeFourFiveJoe"
    assert joeword("aTwoThreeFourFiveSix") == "aTwoThreeJoeFourFiveJoeSixJoe"
    assert joeword("aTwoThreeFourFiveSixSeven") == \
        "aTwoThreeJoeFourFiveJoeSixSevenJoe"
    assert joeword("aTwoThreeFourFiveSixSevenEight") == \
        "aTwoThreeJoeFourFiveJoeSixSevenJoeEightJoe"
    
def joeword(word):
    "make it a joe"
    wordlist = inwordboundary.sub(" ", word).split(" ")
    wordlistlen = len(wordlist)
    insertions = range(3, wordlistlen + 1, 2)
    for i in reversed(insertions):
        wordlist.insert(i, "Joe")
    if len(insertions)==0 or insertions[-1] != wordlistlen:
        wordlist.append("Joe")
    return "".join(wordlist)

def joetext1(text):
    """Joeify the text, standard replacejoes"""
    for frm, to in withinmapping.iteritems():
        text = text.replace(frm, to)
    return text

def joetext2(text):
    """Joeify the text, add further dynamic inWordJoes"""
    textrip = spaceparens.sub(" ", text)
    for word in textrip.split():
        if iscamel.match(word) and (not word in keywords) and (not word in dynamicmapping):
            dynamicmapping[word] = joeword(word)
            print "Added", word, joeword(word)

    for match in classmatch.finditer(text):
        word = match.group(1)
        if (not word in dynamicmapping) and (not word in keywords):
            dynamicmapping[word] = joeword(word)
            print "Added class", word, joeword(word)

    for frm, to in dynamicmapping.iteritems():
        text = text.replace(frm, to)
    return text

def test():
    "test joe"
    print joetext2(joetext1(example))

def main():
    "go joe"
    for line in fileinput.input(inplace=True, backup=".bk"):
        print joetext2(joetext1(line))

if __name__ == '__main__':
    main()

todo
:: use walk to run auto on all java and js files
:: append resulting dict to .joek or so, with timestamp


