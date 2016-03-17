# QUICKSORT
# - the number of comparisons depends on which elements are chosen as pivots
# - rather than counting comparisons one-by-one;
#   when there's a recursive call on a subarray of length m,
#   you should simply add (m-1) to your running total of comparisons.
# - this is because the pivot element is compared to each of the other elements in the subarray in this recursive call

# TODO:  make fct ptrs for choiceOfPivot
#        make fct for swap

# NOTE:  RUN ON CMD LINE as 'python Username MyProgram.py InputFilename'
# using the sys import to retrieve cmd-line args!
import sys
# ATTENTION:  to initialize a fixed integer array, BUT using Lists here for convenience
import array

def loadInputDataFile(inputfile):

    inputInts = []

    try:
        with open(inputfile) as f:
            for line in f:
                linestr = line.strip()
                if linestr:
                   inputInts.append(int(linestr))
    except IOError:
        print "The file does not exist, exiting gracefully"

    return inputInts


# NOTE:  list on heap is modified in-place from the caller
def quicksort(origDataList):

    # ATTENTION:  determine if we should EXIT prior to recursion
    #             ie if LENGTH of list is 1, it's SORTED!

    # NOTE:  return of PTR COPY to HEAP-ALLOCATED LIST is OK on caller!
    if (len(origDataList) <= 1):
        return 0

    # ATTENTION:  RETURN totalComparisons, to CHAIN additions ACROSS recursion levels
    totalComparisons = len(origDataList) - 1
    recursionLevel = 0
    print '$$$$$ Level 0 Comparisons:  {0:d}'.format(totalComparisons)
    totalComparisons += _recurseQuickSort(origDataList, 0, (len(origDataList) - 1), recursionLevel)

    return totalComparisons


# ATTENTION:  use RELATIVE INDEXES to denote which partition the current level of recursion is operating
# against the ORIGINAL dataList; or FULL SIZE
# ATTENTION:  recursionLevel is a STACK var that gets POPPED on return from method
def _recurseQuickSort(origDataList, startIndex, endIndex, recursionLevel):

    # ATTENTION:  increment recursionLevel ONCE at BEGINNING of this method; NOT the CALLER!
    #             INITIAL call is at 0!
    recursionLevel += 1

    # DEBUG
    print '***** ENTRY into recurseQuickSort at RECURSE level:  {0:d}'.format(recursionLevel)
    print 'FULL:  '
    print ','.join(str(x) for x in origDataList)
    print 'Begin-End Indices:  {0:d}, {1:d}'.format(startIndex, endIndex)
    print 'SEGMENT:  '
    print origDataList[startIndex:endIndex+1]

    # ATTENTION:  check for EXIT condition on ENTRY to this method; NOT in CALLER
    #             this handles INVALID condition for index relationship for length of 0 or below
    if (endIndex <= startIndex):
        print "%%% EXIT recursion on 0 or nonsensical length"
        return 0;

    # HUUUGE POINT:  select pivot value RELATIVE to CURRENT segment START;
    # then place it into CURRENT segment START!
    pivotValue, pivotIndex = _choosePivotValue(origDataList, startIndex, endIndex)
    temp = origDataList[startIndex]
    origDataList[startIndex] = origDataList[pivotIndex]
    origDataList[pivotIndex] = temp
    print 'PIVOT chosen {0:d}'.format(pivotValue)

    # ************* HUUUGE POINT:  do coarse swap BEFORE PARTITION-RECURSE to SORT-DETAIL SMALLEST segment! ***********************
    sortedPivotPosition = _coarseSortSwap(origDataList, startIndex, endIndex, recursionLevel)
    print 'RETURNED from coarseSortSwap; SEGMENT (coarsely-sorted); on RECURSE level {0:d}:'.format(recursionLevel)
    print origDataList[startIndex:endIndex+1]

    # ************ HUUUUGE POINT:  need to recurse on partion based on coarse-sorted Pivot Position!
    # ONCE FOUND that pivot value remains STABLE, and stuff changes AROUND it!
    # ALSO  partitionedList is operated on IN-PLACE

    print 'STATS:  startIdx {0:d}, sortedPivotPosition {1:d}, endIdx {2:d}'.format(startIndex, sortedPivotPosition, endIndex)
    # ATTENTION:  counts for comparing pivot to rest of items in segment;
    #        THEN pivot point is STABLE in position, and we process each partition AROUND it recursively
    # ATTENTION:  BLOCKs recursion on 0 or nonsensical length of 1 or below
    if (startIndex < (sortedPivotPosition - 1)):
        print '===== calling LEFT from RECURSE level {0:d}'.format(recursionLevel)
        totalComparisonsLC = (sortedPivotPosition-1) - startIndex
        print '$$$$$ Level {0:d} LC Comparisons:  {1:d}'.format(recursionLevel, totalComparisonsLC)
        totalComparisonsLR = _recurseQuickSort(origDataList, startIndex, (sortedPivotPosition-1), recursionLevel)
        print '$$$$$ Level {0:d} LR Comparisons:  {1:d}'.format(recursionLevel, totalComparisonsLR)

    else:
        print '===== BLOCK LEFT from RECURSE @ level {0:d}'.format(recursionLevel)
        totalComparisonsLC = 0
        totalComparisonsLR = 0

    if ((sortedPivotPosition + 1) < endIndex):
        # NOTE:  comparing pivot to rest of items in segment; or one less than length of segment
        print '===== calling RIGHT from RECURSE level {0:d}'.format(recursionLevel)
        totalComparisonsRC = (endIndex - (sortedPivotPosition + 1))
        print '$$$$$ Level {0:d} RC, RR Comparisons:  {1:d}'.format(recursionLevel, totalComparisonsRC)
        totalComparisonsRR = _recurseQuickSort(origDataList, (sortedPivotPosition+1), endIndex, recursionLevel)
        print '$$$$$ Level {0:d} RR Comparisons:  {1:d}'.format(recursionLevel, totalComparisonsRR)
    else:
        print '===== BLOCK RIGHT from RECURSE @ level {0:d}'.format(recursionLevel)
        totalComparisonsRC = 0
        totalComparisonsRR = 0


    # NOTE:  add in NESTED RECURSIVE contributions LR, RR
    #        add in CURRENT level contributions
    aggregateComparisons = totalComparisonsLC + totalComparisonsLR + totalComparisonsRC + totalComparisonsRR
    print '$$$$$ Level {0:d} AGGREGATE comparisons sum to:  {1:d}'.format(recursionLevel, aggregateComparisons)
    print 'for SEGMENT:  '
    print origDataList[startIndex:endIndex+1]



    # ATTENTION:  return of partitionedList NOT needed, as STACK PTR COPY to HEAP-ALLOCATED space from CLIENT CALLER is modified
    #             ie input itself is modified

    return aggregateComparisons

def _choosePivotValue(origDataList, startIndex, endIndex):
    # TODO: pass in method pointer to parameterize pivot value pick strategy
    # FIRST ELEMENT
    pivotIndex = startIndex
    # LAST ELEMENT
    # pivotIndex = endIndex
    pivotValue = origDataList[pivotIndex]
    return (pivotValue, pivotIndex)

# TODO:  use method pointers in quicksort calling method to parameterize pivot-choice algo!
# ASSUMPTION is that pivot value ALREADY figured previously, was also previously put in FIRST array value!
# INVARIANT:  partitionScan points to FIRST element of data stream GREATER THAN pivotValue; everything before that is LESS THAN pivotValue
# NOTE0:  use INDEXES to denote which partition the current level of recursion is operating on ORIGINAL dataList; or FULL SIZE
# NOTE1:  all elements on left side of pivot_scan are less than pivot value
#         a_recurse_QuickSort(origDataList, startIndex, endIndex)ll elements equal, or on right side of pivot_scan are greater than pivot value
# NOTE2:  all elements on left side of fresh_data_bound have been partitioned,
#         all elements on right side of new_data_bound still need to be examined
def _coarseSortSwap(dataList, startIndex, endIndex, recursionLevel):

    # DEBUG
    # print'--- ENTERED coarseSortSwap  ---'
    # print 'fullDataList:  '
    # print ','.join(str(x) for x in dataList)
    # print'Begin-End Indices:  {0:d}, {1:d}'.format(startIndex, endIndex)
    # print'pivotValue'
    # print '{0:d}'.format(dataList[startIndex])
    # print 'segment to sort:  '
    # print dataList[startIndex:(endIndex-startIndex+1)]

    # ASSUMPTION is that pivotValue was previously set to FIRST element
    pivotValue = dataList[startIndex]

    # start scanning for fresh data from point 1 over from pivot point
    # ATTENTION:  want to retain partitionScan; so assign here
    partitionScan = (startIndex + 1)
    newDataScan = (startIndex + 1)
    # ATTENTION:  don't use RANGE as we are INDEPENDENTLY ADJUSTING SCAN PTR iteration!
    # for partitionScan in range(afterPivotIndex, endIndex):
    # for newDataScan in range(afterPivotIndex, endIndex):
    while ( (newDataScan <= endIndex) and (partitionScan <= endIndex)):

            # CASE 1:  we detect a value LESS than the pivot, and  GROW the less-than segment by moving the partitionScan
            if (dataList[newDataScan] < pivotValue):

                # CASE 1.1:  we currently have SOME processed data GREATER than pivotValue, i.e. newDataScan > partitionScan
                if (newDataScan > partitionScan):
                    # ATTENTION:  key point is that if new data value is SMALLER than pivot,
                    #             we need to SWAP it into the BOTTOM of the LARGER-THAN partition to grow the LOWER-THAN partition,
                    #             thus moving that first LARGER-THAN item to the END of the LARGER-THAN partition!
                    temp = dataList[partitionScan]
                    dataList[partitionScan] = dataList[newDataScan]
                    dataList[newDataScan] = temp

                # CASE 1.2:  we have NO processed data GREATER than pivot value
                #            NO swap is needed, and it's sufficient to just advance the partition scan
                partitionScan += 1

            # CASE 2:  we detect a value GREATER than the pivot,
            #          so we DON'T need to do anything here as the LESS-THAN segment ramains unchanged,
            #          and we just need to advance the scanning pointer
            #          to expand the GREATER-THAN segment!

            # in any case, advance the scanning pointer
            newDataScan += 1

    # print 'BEFORE swap pivot value IN-PLACE; AT RECURSE level {0:d}'.format(recursionLevel)
    # print dataList[startIndex:(endIndex+1)]

    # KEY:  put pivot value back IN-PLACE without messing up order, NOR needing to allocate auxiliary storage
    # ATTENTION:  this maintains the invariant that lower half is less than pivot
    # CASE 2.1:  we have found ALL data VALUES LESS THAN so put PIVOT value at the END
    if (partitionScan > endIndex):
        # ATTENTION:  SHIFT ALL data DOWN one spot WITHOUT dropping anything; so iterate UP
        # TODO:  WHY is the following not iterating UP?
        # for srcIndex in range(startIndex, (endIndex-1), 1):
        srcIndex = startIndex

        while (srcIndex <= (endIndex-1)):
            dataList[srcIndex] = dataList[(srcIndex+1)]
            srcIndex += 1

        # NOTE, put blank line AFTER while loop
        dataList[endIndex] = pivotValue
    # CASE 2.2:  we have found ALL data VALUES GREATER THAN so LEAVE LIST ALONE
    elif (partitionScan == (startIndex + 1)):
        pass
    # CASE 2.3:  we HAVE found SOME data GREATER than pivot value, AND SOME data LESS than pivot value
    #            so put PIVOT at the END of the LESS THAN portion of the list, then append the GREATER THAN portion
    else:
        # ATTENTION:  SHIFT LESS-THAN data DOWN one spot WITHOUT dropping anything; so iterate UP
        # for srcIndex in range(startIndex, (partitionScan - 1), 1):
        srcIndex = startIndex

        while (srcIndex < (partitionScan-1)):
            dataList[srcIndex] = dataList[(srcIndex+1)]
            srcIndex += 1

        # NOTE, put blank line AFTER while loop
        # PLACE the pivot value here
        dataList[(partitionScan-1)] = pivotValue

    # print'--- RETURN OUT of coarseSortSwap ---'
    # print 'fullDataList:  '
    # print ','.join(str(x) for x in dataList)
    # print 'segment sorted:  '
    # print dataList[startIndex:(endIndex-startIndex + 1)]

    # Adivyabhide@gmail.comTTENTION:  the original dataList (on HEAP) will be self-modified
    sortedPivotPosition = partitionScan - 1
    return sortedPivotPosition

def main(args):

    # print("\n\nWELCOME {0}!   Sorts data from file from SECOND input argument if given.  Otherwise defaults to /data/TenIntegerArray.txt.\n".format(args[1]))

    # NOTE:  TEST CASES
    # 10 => 25, NOW I get 25
    # 10reverse => I get 45
    # 100 => 615 => BUT I get 647

    # if no filename supplied, enter it here
    if ((len(args) < 3) or args[2] == None):
        inputfile = "../data/oddreverse.txt"
    else:
        inputfile = args[1]

    inputDataList = loadInputDataFile(inputfile)

    print '***** input numbers read *****'
    print ','.join(str(x) for x in inputDataList)
    print '\n'

    totalComparisons = quicksort(inputDataList)

    print '***** output numbers sorted *****'
    print ','.join(str(x) for x in inputDataList)

    print '***** TOTAL comparisons *****'
    print '{0:d}'.format(totalComparisons)
    print '\n'

# ATTENTION:  main entrypoint, for Python to emulate Java main entrypoint
if __name__ == '__main__':
    main(sys.argv)



