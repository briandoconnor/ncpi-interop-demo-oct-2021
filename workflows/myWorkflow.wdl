version 1.0

workflow coverage {

    input {
      File fasta
      File cram
      Int gt_coverage
    }

    call indexTask {
      input:
        cram=cram
    }

    call coverageTask {
      input:
        fasta=fasta, cram=cram, crai=indexTask.crai, gt_coverage=gt_coverage
    }

    output {
      Float chrX = coverageTask.chrX
      Float chrY = coverageTask.chrY
      Float chr19 = coverageTask.chr19
      File global_dist = coverageTask.global_dist
      File regions = coverageTask.regions
      File region_dist = coverageTask.region_dist
      File regions_index = coverageTask.regions_index
    }
}

task indexTask {

    input {
      File cram
      String localCram = sub(basename(cram), ":", "_")
    }

    runtime {
      docker: "staphb/samtools:1.13"
      cpu: 4
      memory: "8G"
      disks: "local-disk 300 SSD"
    }
    command <<<
        set -e -o pipefail
        cp ~{cram} ~{basename(cram)}
        samtools index ~{basename(cram)} ~{basename(cram)}.crai
    >>>

    output {
      File crai = glob('*.crai')[0]
    }

}

task coverageTask {

    input {
      File fasta
      File cram
      File crai
      Int gt_coverage
    }
    runtime {
      docker: "quay.io/biocontainers/mosdepth:0.2.4--he527e40_0"
      cpu: 4
      memory: "8G"
      disks: "local-disk 300 SSD"
    }
    command <<<
        cp ~{crai} ~{basename(cram)}.crai && \
        cp ~{cram} ~{basename(cram)} && \
        mosdepth -n --fast-mode -t 4 --by 1000 sample -f ~{fasta} ~{basename(cram)} && \
        cat sample.mosdepth.global.dist.txt | grep chrX$'\t'~{gt_coverage}$'\t'  | awk '{print $3}' > chrX.txt && \
        cat sample.mosdepth.global.dist.txt | grep  chrY$'\t'~{gt_coverage}$'\t'  | awk '{print $3}' > chrY.txt && \
        cat sample.mosdepth.global.dist.txt | grep  chr19$'\t'~{gt_coverage}$'\t'  | awk '{print $3}' > chr19.txt
    >>>
    output {
      Float chrX = read_float("chrX.txt")
      Float chrY = read_float("chrY.txt")
      Float chr19 = read_float("chr19.txt")
      File global_dist = "sample.mosdepth.global.dist.txt"
      File regions = "sample.regions.bed.gz"
      File region_dist = "sample.mosdepth.region.dist.txt"
      File regions_index = "sample.regions.bed.gz.csi"
    }
}
