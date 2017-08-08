# Change this to use plain scanf instead of fscanf to see what the difference is.

# Notes

## input
```bash
./ex24 <<EOF
Ekeyme
Mo
27
5
999999999

EOF
```

## results of fscanf version
----- RESULTS -----
First Name: Ekeyme
Last Name: Mo
Age: 27
Eyes: Other
Income: 1000000000.000000

## results of scanf version
----- RESULTS -----
First Name: Ekeyme
Last Name: Mo
Age: 27
Eyes: Other
Income: 1000000000.000000

# Conclusion
I think the effect of scanf version is the same with the fscanf version.
