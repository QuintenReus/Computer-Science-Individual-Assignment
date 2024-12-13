This code is created to perform duplicate detection on a set of TVs. The methods are based on the papers below and include locality sensitive hashing, multi-component similarity method, minhashing and more. The code is separated into different Python files.

There are two different main files. The main_LSH run the code, including bootstraps, for isolating the performance of the LSH method. Here the duplicates are set to be the candidate pairs proposed by LSH. The main_MSM.py file runs the full code including the MSMP+ calculations. Furthermore, there is a test_set.py that allows you to create a subsample of the data that can be used for testing.


1. De Bakker, M., Frasincar, F., Vandic, D.: A hybrid model words-driven approach
for web product duplicate detection. In: Advanced Information Systems Engineer-
ing: 25th International Conference, CAiSE 2013, Valencia, Spain, June 17-21, 2013.
Proceedings 25. pp. 149–161. Springer (2013)
2. Hartveld, A., van Keulen, M., Mathol, D., van Noort, T., Plaatsman, T., Frasin-
car, F., Schouten, K.: An lsh-based model-words-driven product duplicate detection
method. In: International Conference on Advanced Information Systems Engineer-
ing. pp. 409–423. Springer (2018)
3. Van Bezu, R., Borst, S., Rijkse, R., Verhagen, J., Vandic, D., Frasincar, F.: Multi-
component similarity method for web product duplicate detection. In: Proceedings
of the 30th annual ACM symposium on applied computing. pp. 761–768 (2015)
4. Van Dam, I., van Ginkel, G., Kuipers, W., Nijenhuis, N., Vandic, D., Frasincar, F.:
Duplicate detection in web shops using lsh to reduce the number of computations.
In: Proceedings of the 31st Annual ACM Symposium on Applied Computing. pp.
772–779 (2016)
5. Vandic, D., Van Dam, J.W., Frasincar, F.: Faceted product search powered by the
semantic web. Decision Support Systems 53(3), 425–437 (2012)
