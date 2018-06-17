# Barcode-design
## attention
> generaly, this code running time is less than 0.2s, if its running time > 1s, try it again. because of the random generated matrix.
### usage
> python barcode_design.py
### meet condition
1. hamming distance >= 3 between sequence
2. no 3 continuous bases like AAA, CCC, GGG, TTT
3. 16 seqences are clustered into a group, and bases ratio in every location in each group > 12.5%  
