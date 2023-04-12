<script>
export default {
  name: 'RenderCol',
  functional: true,
  props: {
    row: Object,
    render: Function,
    index: Number,
    column: {
      type: Object,
      default: null
    }
  },
  render(h, ctx) {
    const params = {
      row: ctx.props.row,
      index: ctx.props.index
    }
    if (ctx.props.column) params.column = ctx.props.column
    return ctx.props.render(ctx.props?.row[ctx.props?.column?.prop], ctx.props.row, ctx.props.index)
  }
}
</script>
