import sys
import time
import numpy as np
import heapq

def main():
	(training_data,testing_data) = parse_data() if len(sys.argv) != 3 else parse_data(sys.argv[1],sys.argv[2])
	normalize(training_data,testing_data)
	for k in [i*2+1 for i in xrange(0,26)]:
	   	print "k =",k
		print "---------------------"
		cv_count = 0
		train_error_count = 0
		for i in xrange(0,len(training_data)):
	   		answer = knn(training_data[:i]+training_data[i+1:],training_data[i][1:],k)
	   		if (answer != int(training_data[i][0])): cv_count = cv_count + 1
			answer = knn(training_data,training_data[i][1:],k)
			if (answer != int(training_data[i][0])): train_error_count = train_error_count + 1
		test_error_count = 0
		for i in xrange(0,len(testing_data)):
		   	answer = knn(training_data,testing_data[i][1:],k)
			if (answer != int(testing_data[i][0])): test_error_count = test_error_count + 1
		
		print "training error count:",train_error_count,"/",len(training_data),"=",float(train_error_count*100)/float(len(training_data)),"%"	      
		print "testing error count:",test_error_count,"/",len(testing_data),"=",float(test_error_count*100)/float(len(testing_data)),"%"	      
		print "leave-one-out cross-validation error:",cv_count,"/",len(training_data),"=",float(cv_count*100)/float(len(training_data)),"%"
		

def parse_data(training_filename = "knn_train.csv", testing_filename = "knn_test.csv"):
	training_file = open(training_filename, 'r')
	test_file = open(testing_filename, 'r')
	
	start_time0 = time.clock()
	training_data = [[float(item) for item in line.split(',')] for line in training_file.read().splitlines()]
	testing_data = [[float(item) for item in line.split(',')] for line in test_file.read().splitlines()]
	training_file.close()
	test_file.close()
	return (training_data, testing_data)

def normalize(training_data,testing_data):
   	mins = training_data[0][1:]
	maxs = training_data[0][1:]
	for point in training_data[1:]:
	   new_mins = [min(mins[i],point[i+1]) for i in xrange(0,len(mins))]
	   new_maxs = [max(maxs[i],point[i+1]) for i in xrange(0,len(maxs))]
	   mins = new_mins
	   maxs = new_maxs
	for point in training_data:
	   for i in xrange(1,len(point)):
	      point[i] = (point[i]-mins[i-1])/(maxs[i-1]-mins[i-1])
	for point in testing_data:
	   for i in xrange(1,len(point)):
	      point[i] = (point[i]-mins[i-1])/(maxs[i-1]-mins[i-1])

#returns 1 or -1
def knn(training_data,point,k):
   return 1 if sum([points[1] for points in heapq.nsmallest(k,[[np.linalg.norm([data[i+1]-point[i] for i in xrange(0,len(point))]),data[0]] for data in training_data])]) > 0 else -1

if __name__ == "__main__": main()
