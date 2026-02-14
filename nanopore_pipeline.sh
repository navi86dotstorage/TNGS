#!/bin/bash

#scripts="/home/nirtbact/softwares/nanopore_pipeline_files"
scripts="/home/nirtbact/softwares/nanopore_pipeline_files"
for fold in *; do

	    if [ -d "$fold" ]; then

	        echo -e "\n   Running analysis for "$fold"...\n"
	    
    		cd $fold

		cat *.fastq.gz > $fold.fastq.gz

		
		if [ "$?" != 0 ];

		then

			echo -e "\n\n...error no reads!!!\n.....check folder $fold\n\n"
	
			exit 1

		else

			echo -e "\n...$fold reads ready...\n\n"
		
		fi

		echo -e "\n\n...started variant analysis pipeline...\n\n"

		
		minimap2 /home/nirtbact/softwares/nanopore_pipeline_files/NC_000962.3.fa.gz "$fold".fastq.gz -axmap-ont &>>tmp1 > alignment.sam


		samtools view -bS alignment.sam > alignment.bam


		samtools sort alignment.bam -o alignment_sort.bam


		bcftools mpileup -Ov -f /home/nirtbact/softwares/nanopore_pipeline_files/NC_000962.3.fa alignment_sort.bam | bcftools call -mv -o "$fold".vcf &>>tmp2


		echo -e "\n\n...Starting lineage prediction...\n\n"	

#		mkdir $fold"_lineage"

		mkdir $fold"_variant"
	
#		cd $fold"_lineage"
	
		python2 $scripts/RD-Analyzer.py -o $fold $fold".fastq.gz" &>tmp3 || echo "error in program1! aborted" exit 1 &
	
		mv *.vcf $fold"_variant"
	
		cd $fold"_variant"
			
		echo -e "\n\n...Running the variant annotation...\n\n"	

		python2 $scripts/filtervcf4.py $fold".vcf" $fold
	
		python2 $scripts/ResPred_ann_v5.py $scripts/"refdict_v5" $scripts/"MtDb5sPhyFann" $scripts/"coord_v3" $fold"_filtered.vcf" $fold $scripts/"gene_list"

		python2 $scripts/pick_rest.py $scripts/"MtDb5sPhyFann" $fold"_others" $fold

			
		echo -e "\n\n...Finished the variant calling and annotation successfully...\n\n"
	

#		rm ../$fold"_lineage"/"tmp3"

		cd ../
	
#		python2 $scripts/detectphyl_v2.py $scripts/"PhyloFranc" $fold"_variant"/$fold"_others" $fold"_result" $fold"_variant" $fold
	
#		cd ../

		python3 /home/nirtbact/softwares/snpit/bin/snpit-run.py --input $fold"_variant"/$fold".vcf" --output $fold"_variant"/$fold"_lineage"

		wait		

		echo -e "....completed analysis for $fold\n\n"
		
		mkdir analysis

		mv $fold* analysis

#		rm alignment*

		rm tmp*

		cd ..
		
fi 

done
