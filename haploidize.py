import random
import argparse

def haploidize_vcf(input_file, output_file):
    with open(input_file, 'r') as input_vcf, open(output_file, 'w') as output_vcf:
        for line in input_vcf:
            if line.startswith('#'):
                #Write header lines 
                output_vcf.write(line)
            else:
                #Parse variant information
                fields = line.strip().split('\t')
                genotypes = fields[9:]  #Genotypes start from column 10

                #Modify the genotype information
                haploid_genotypes = []
                for genotype in genotypes:
                    alleles = genotype.split(':')[0].split('|')
                    
                    #Replace '1|0' with either '0|0' or '1|1'
                    if '1|0' in alleles:
                        new_genotype = random.choice(['0|0', '1|1'])
                    else:
                        #If not '1|0', ensure the format is '0|0' or '1|1'
                        selected_allele = random.choice(alleles)
                        new_genotype = f"{selected_allele}|{selected_allele}"
                    
                    haploid_genotypes.append(new_genotype)

                #Update the genotype information
                fields[9:] = haploid_genotypes

                #Write the modified variant to the output file
                output_vcf.write('\t'.join(fields) + '\n')

def main():
    parser = argparse.ArgumentParser(description='Haploidize a VCF file')
    parser.add_argument('input_file', help='Path to the input VCF file')
    parser.add_argument('output_file', help='Path to the output VCF file')
    args = parser.parse_args()

    haploidize_vcf(args.input_file, args.output_file)

if __name__ == '__main__':
    main()
