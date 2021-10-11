version 1.0

workflow coverage {

    input {
      File coverage
      Int gt_coverage
    }

    call coverageTask {
      input:
        coverage=coverage, gt_coverage=gt_coverage
    }

    output {
      Float chrX = coverageTask.chrX
      Float chrY = coverageTask.chrY
      Float chr19 = coverageTask.chr19
    }
}

task coverageTask {

    input {
      File coverage
      Int gt_coverage
    }
    runtime {
      docker: "quay.io/biocontainers/mosdepth:0.2.4--he527e40_0"
    }
    command <<<
        cat ~{coverage} | grep chrX$'\t'~{gt_coverage}$'\t' | awk '{print $3}' > chrX.txt
        cat ~{coverage} | grep chrY$'\t'~{gt_coverage}$'\t' > chrY.txt
        cat ~{coverage} | grep chr19$'\t'~{gt_coverage}$'\t' | awk '{print $3}' > chr19.txt
    >>>
    output {
      Float chrX = read_float("chrX.txt")
      Float chrY = read_float("chrY.txt")
      Float chr19 = read_float("chr19.txt")
    }
}
