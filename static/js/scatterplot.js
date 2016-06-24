cols = _.filter(_.keys(grid), x => !/_loop/.test(x))
arrarr = _.map(_.keys(grid._loop_id), x => _.map(cols, y => grid[y][x]) );


var tsnechart = echarts.init(document.getElementById('charts'), theme);
tsnechart.setOption({
  title: {
    text: 'tSNE projection',
    subtext: 'of completed iterations'
  },
  tooltip: {
    trigger: 'axis',
    showDelay: 0,
    axisPointer: {
      type: 'cross',
      lineStyle: {
        type: 'dashed',
        width: 1
      }
    }
  },
  legend: {
    data: ['complete']
  },
  toolbox: {
    show: true,
    feature: {
      saveAsImage: {
        show: true,
        title: "Save Image"
      }
    }
  },
  xAxis: [{
    type: 'value',
    show: true
  }],
  yAxis: [{
    type: 'value',
    show: true
  }],
  series: [{
    name: 'complete',
    type: 'scatter',
    tooltip: {
      trigger: 'item',
      formatter: function(params) {
        if (params.value.length > 1) {
          var id = params.dataIndex;
          return 'loop_id: ' + _.values(grid._loop_id)[id] + ' :<br/>' + _.reduce(_.map(cols, x => x + ': ' + _.values(grid[x])[id].toFixed(2) + ';'), (sum, n) => sum + ' ' + n, '');
        }
      }
    },
    data: Y
  }]
});
