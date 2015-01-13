#############
#  mapreduce_simple_stats_example.py
#
#  Mapreduce pipeline to extract fields of interest from log files
#
#  Args:
#    At the command line, type
#    python mr_simple_stats_example.py *.log > out.txt
#
# Returns:
#    List of elements from the log files (e.g. IP addresses), and the number
#    of times they occurred.  
#
#    The output file is typically of moderate size, a few MB, and so 
#    can be processed in a statistics environment like R on a single machine.
#
#  Author:  G. Ryder, Menlo Park, 2013
#
#  Acknowledgements: https://pythonhosted.org/mrjob    
#
#############

from mrjob.job import MRJob
import re

#--Select one of the regular expressions below to use in the mapreduce job
WORD_RE = re.compile(r"[\w']+") #--matches all words
DATE_RE = re.compile('(\d*\/[a-zA-Z]*\/\d*:\d*:\d*:\d*\s\+\d*)') #--matches the date
IP_RE = re.compile('(\d+\.\d+\.\d+\.\d+)') #--matches the IP address
SCREEN_RE = re.compile('(GET\s\/[^\s]*\s)') #--matches the web page component being retrieved
#--The one below captures date, IP and screen, with some text to discard in the middle
ALL_FIELDS_RE = re.compile('(\d*\/[a-zA-Z]*\/\d*:\d*:\d*:\d*\s\+\d*.*GET\s\/[^\s]*\s)')

#/Library/Java/JavaVirtualMachines/jdk1.7.0_71.jdk/Contents/Home


class MRStatistics(MRJob):

    def mapper_step(self, _, line):
        # Yield a result for this regex
        # for word in <regex name>.findall(line):
        for item in SCREEN_RE.findall(line):
            yield (item.lower(), 1)

    def combiner_step(self, item, counts):
        # Sum the occurrences of each element identified in the mapper.
        yield (item, sum(counts))

    def reducer_step1(self, item, counts):
        # Send all (num_occurrences, word) pairs to the same reducer.
        yield None, (sum(counts), item)

    def reducer_step2(self, _, item_count_pairs):
        # Each item of item_count_pairs is (count, item),
        # so yielding one results in key=counts, value=item.
        for item in item_count_pairs:
            print str(item)



    def steps(self):
        return [
            self.mr(mapper=self.mapper_step,
                    combiner=self.combiner_step,
                    reducer=self.reducer_step1),
            self.mr(reducer=self.reducer_step2)
        ]


if __name__ == '__main__':
    MRStatistics.run()