singularity: "docker://rkibioinf/samtools:1.11--b05ccf8"

def input_sortBam(wildcards):
    if PRIMER:
        return os.path.join(DATAFOLDER["mapping"], "{sample}", "{sample}.primerclipped.bam")
    else:
        return os.path.join(DATAFOLDER["mapping"], "{sample}", "{sample}.bam")

rule sortBam:
    input:
        input_sortBam
    output:
        os.path.join(DATAFOLDER["mapping"], "{sample}", "{sample}.sort.bam")
    log:
        os.path.join(DATAFOLDER["logs"], "mapping", "{sample}.sort.log")
    conda:
        "../envs/samtools.yaml"
    threads:
        10
    shell:
        r"""
            samtools sort -@ {threads} -o {output} {input} &> {log}
        """