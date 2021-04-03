version 1.0

task download {

input {
  String fileid
  String token
  String outputfilename
}

command {
  python /usr/local/bin/download.py --token ${token} --fileid ${fileid} --outputdir .
}

output {
  File outputfile = "${outputfilename}"
}

runtime {
 docker: "quay.io/briandoconnor/ncpi-interop-demo:1.0"
 cpu: 1
 memory: "512 MB"
 disks: "local-disk 375 SSD"
}
}

workflow gmkf_download {

input {
  String fileid
  String token
  String outputfilename
}

call download { input: fileid=fileid, token=token, outputfilename=outputfilename  }

output {
  File outputfile = download.outputfile
}

}
