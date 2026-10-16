# Project 9: Sampling, Confidence Intervals and Generalizability in Diabetes

## 1. Introduction

Sampling is important in medical research because researchers usually cannot measure every individual in a population.

A sample is therefore used to estimate unknown characteristics of the population.

In this project, the Glucose variable from the Pima Indians Diabetes Dataset was used to study:

- Population and sample statistics
- Sampling error
- Standard Error
- 95% Confidence Intervals
- Sample size
- Central Limit Theorem

---

## 2. Population

For this project, the complete dataset was treated as the population.

Population size:

768

Population mean of Glucose:

120.8945

Population standard deviation:

31.9518

The population mean is a parameter because it describes the full population used in this project.

A mean calculated from a random sample is a statistic.

---

## 3. Sampling

Random samples were selected without replacement.

The following sample sizes were studied:

- 10
- 30
- 50
- 100
- 300

Because each sample contains only part of the population, its mean is not expected to be exactly equal to the population mean.

This difference is an example of sampling variability.

---

## 4. Standard Error

For each sample, the Standard Error of the mean was calculated as:

SE = s / sqrt(n)

where:

- s is the sample standard deviation
- n is the sample size

Standard Error represents the uncertainty of the sample mean as an estimate of the population mean.

As sample size increases, Standard Error generally becomes smaller.

---

## 5. 95% Confidence Interval

The 95% Confidence Interval was calculated using the t distribution:

CI = sample mean ± t critical × SE

The t distribution was used because the population standard deviation is not assumed to be known when calculating the interval from a sample.

---

## 6. Results

|   Sample_Size |   Sample_Mean |   Sample_SD |      SE |   CI_Lower |   CI_Upper |   CI_Width | Contains_Population_Mean   |
|--------------:|--------------:|------------:|--------:|-----------:|-----------:|-----------:|:---------------------------|
|            10 |       133.8   |     41.8749 | 13.242  |    103.844 |    163.756 |    59.9111 | True                       |
|            30 |       125.433 |     30.891  |  5.6399 |    113.898 |    136.968 |    23.0698 | True                       |
|            50 |       113.88  |     31.0527 |  4.3915 |    105.055 |    122.705 |    17.6502 | True                       |
|           100 |       121.15  |     35.8911 |  3.5891 |    114.028 |    128.272 |    14.2431 | True                       |
|           300 |       121.137 |     30.9434 |  1.7865 |    117.621 |    124.652 |     7.0315 | True                       |

The results show that sample means vary because of random sampling.

In general, larger samples produce smaller Standard Errors and narrower Confidence Intervals.

Therefore, larger samples usually provide more precise estimates of the population mean.

---

## 7. Confidence Interval Width

The plot `ci_width_vs_sample_size.png` shows the relationship between sample size and Confidence Interval width.

As the sample size increases, the Confidence Interval generally becomes narrower.

This occurs because:

SE = s / sqrt(n)

As n increases, the denominator becomes larger and SE decreases.

---

## 8. Population Mean and Confidence Intervals

The plot `ci_intervals.png` compares the sample mean and 95% Confidence Interval for each sample size with the population mean.

A Confidence Interval may or may not contain the true population mean in a particular sample.

A 95% Confidence Interval does not mean that there is a 95% probability that the fixed population mean is inside one particular calculated interval.

Instead, if the sampling procedure were repeated many times, approximately 95% of intervals constructed by this method would contain the true population mean.

---

## 9. Central Limit Theorem

To examine the Central Limit Theorem, 1000 random samples were generated.

Each sample contained 50 observations.

The mean Glucose value was calculated for every sample.

Mean of the 1000 sample means:

120.7780

Standard deviation of sample means:

4.2228

The histogram of sample means is stored in:

`clt_sample_means.png`

The sampling distribution of the mean tends to be more approximately Normal than the distribution of individual observations.

Its center is also close to the population mean.

This demonstrates the Central Limit Theorem.

---

## 10. Analytical Questions

### 1. Why is the sample mean not exactly equal to the population mean?

A random sample contains only part of the population.

Different random samples contain different observations, so their means vary.

This is called sampling variability.

---

### 2. What happens to CI width when sample size increases?

The Confidence Interval generally becomes narrower.

Larger samples reduce the Standard Error and increase the precision of the estimate.

---

### 3. What is the difference between SD and SE?

Standard Deviation describes the variability of individual observations.

Standard Error describes the variability or uncertainty of the sample mean.

SD describes the data.

SE describes the precision of the estimated mean.

---

### 4. What is the correct interpretation of a 95% CI?

If the same sampling and Confidence Interval procedure were repeated many times, approximately 95% of the calculated intervals would contain the true population mean.

---

### 5. What does the Central Limit Theorem say?

As sample size becomes sufficiently large, the sampling distribution of the sample mean tends toward a Normal distribution under appropriate conditions.

Its center approaches the population mean.

---

### 6. Does a 95% CI always contain the population mean?

No.

A particular 95% Confidence Interval can miss the true population mean.

The 95% refers to the long-run performance of the interval-building procedure.

---

### 7. Why can a large but biased sample be misleading?

A large sample reduces random sampling error, but it does not automatically remove systematic bias.

If the sample is not representative of the target population, a very large sample can still provide a precise but incorrect estimate.

---

## 11. Limitations

The full dataset was treated as the population for educational purposes.

In real medical research, the observed dataset is normally itself a sample from a much larger target population.

The quality of an estimate depends not only on sample size but also on:

- Sampling method
- Representativeness
- Measurement quality
- Missing data
- Selection bias

A large sample cannot automatically correct these problems.

---

## 12. Conclusion

This project demonstrated the relationship between sample size, Standard Error and Confidence Interval width.

Small samples showed greater uncertainty.

Larger samples generally produced narrower Confidence Intervals and more precise estimates.

The simulation of 1000 sample means also demonstrated the Central Limit Theorem.

Therefore, both sample size and sampling quality are important when generalizing medical research results from a sample to a population.