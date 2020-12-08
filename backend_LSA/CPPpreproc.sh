# This code compiles the code using g++, but terminates after the pre-processing step.
# This does two things: remove all macros (such as #define and #include) and replaces them with the
# raw code in a file. Sending the output to temp creates a large file with this.
g++ -E $1 > temp
# Now, we don't want the massive amounts of code which are present because of the replacement of the
# (#include) macros - not replacing them results in a file of over 100000 lines.
# https://gcc.gnu.org/onlinedocs/cpp/Preprocessor-Output.html
# Going through the official documentation shows that when we start a section caused by a #include,
# it should be of the form
# # linenum "library name" 1 3
# and ends with
# # linennum "file name" 2
# Use sed to delete all the intermediate lines
sed '/^# [0-9]* ".*" 1 3/,/# [0-9]* ".*" 2$/d' temp > temp1
# There finally remain some excess lines that begin with a # that we do not require.
# Use sed to delete these unnecessary lines
sed '/^#/d' temp1 > temp
# Delete the temporary created file
rm temp1