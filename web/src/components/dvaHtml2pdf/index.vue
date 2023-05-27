<template>
  <div>
    <div style="position: absolute;z-index: 10000">
      <el-button
        type="success"
        round
        size="small"
        v-if="downloadButtonShow"
        :style="downloadButtonStyle"
        @click="generateReport"
        :loading="downloadLoading"
      >{{ downloadButtonTitle }}
      </el-button>
      <el-button
        type="primary"
        round
        size="small"
        v-if="previewButtonShow"
        style="position: fixed; right: 50px; bottom: 70px"
        @click="previewPdf"
        :loading="previewLoading"
      >{{ previewButtonTitle }}
      </el-button>
    </div>
    <vue-html2pdf
      :show-layout="true"
      :float-layout="false"
      :enable-download="false"
      :preview-modal="preview"
      :filename="filename"
      :paginate-elements-by-height="1100"
      :pdf-quality="2"
      pdf-format="a4"
      pdf-orientation="portrait"
      pdf-content-width="100%"
      :manual-pagination="true"
      :html-to-pdf-options="{ margin: [5, 5, 0, 5] }"
      @beforeDownload="beforeDownload($event)"
      ref="html2Pdf"
    >
      <section slot="pdf-content">
        <slot></slot>
      </section>
    </vue-html2pdf>
  </div>
</template>

<script>
import SongtiSCBlack from '@/assets/fonts/SongtiSCBlack'
import VueHtml2pdf from 'vue-html2pdf'

export default {
  name: 'dvaHtml2pdf',
  components: {
    VueHtml2pdf
  },
  props: {
    filename: { // 导出pdf文件名称
      type: String,
      require: true
    },
    company: { // 企业名称
      type: String,
      default: 'xxx '
    },
    // 是否显示下载按钮
    downloadButtonShow: {
      type: Boolean,
      default: true
    },
    // 下载按钮样式
    downloadButtonStyle: {
      type: Object,
      default () {
        return {
          position: 'fixed', right: '50px', bottom: '30px'
        }
      }
    },
    // 下载按钮标题
    downloadButtonTitle: {
      type: String,
      default: '下载报告'
    },
    // 是否显示预览按钮
    previewButtonShow: {
      type: Boolean,
      default: true
    },
    // 预览按钮样式
    previewButtonStyle: {
      type: Object,
      default () {
        return {
          position: 'fixed', right: '50px', bottom: '70px'
        }
      }
    },
    // 预览按钮标题
    previewButtonTitle: {
      type: String,
      default: '预览报告'
    }
  },
  data () {
    return {
      preview: false,
      downloadLoading: false,
      previewLoading: false
    }
  },
  created () {
  },
  mounted () {
  },
  methods: {
    async beforeDownload ({ html2pdf, options, pdfContent }) {
      if (this.preview) return
      await html2pdf()
        .set(options)
        .from(pdfContent)
        .toPdf()
        .get('pdf')
        .then((pdf) => {
          const totalPages = pdf.internal.getNumberOfPages()
          for (let i = 1; i <= totalPages; i++) {
            pdf.setPage(i)
            pdf.addFileToVFS('MyFont.ttf', SongtiSCBlack)
            pdf.addFont('MyFont.ttf', 'MyFont', 'normal')
            pdf.setFont('MyFont')
            pdf.setFontSize(10)
            pdf.setTextColor(150)
            pdf.text(
              '第 ' + i + '页  共 ' + totalPages + '页',
              pdf.internal.pageSize.getWidth() * 0.45,
              pdf.internal.pageSize.getHeight() - 2
            )
            pdf.text(
              this.company,
              pdf.internal.pageSize.getWidth() * 0.79,
              pdf.internal.pageSize.getHeight() - 2
            )
          }
        })
        .save(this.filename)
    },
    generateReport () {
      this.preview = false
      this.downloadLoading = true
      this.$nextTick(() => {
        this.$refs.html2Pdf.generatePdf()
        const _this = this
        setTimeout(function () {
          _this.downloadLoading = false
        }, 4000)
      })
    },
    previewPdf () {
      this.preview = true
      this.previewLoading = true
      this.$nextTick(() => {
        this.$refs.html2Pdf.generatePdf()
        const _this = this
        setTimeout(function () {
          _this.previewLoading = false
        }, 4000)
      })
    }
  }

}
</script>

<style scoped>

</style>
