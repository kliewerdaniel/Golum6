const AIContentWidget = createClass({
    handleGenerate: function() {
      const title = this.props.value.get('title') || '';
      fetch('/generate-ai-content', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title }),
      })
      .then(response => response.json())
      .then(data => {
        this.props.onChange({
          title: title,
          body: data.content,
          ai_comments: data.comments,
        });
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    },
  
    render: function() {
      const {forID, classNameWrapper, value, onChange} = this.props;
      return h('div', {className: classNameWrapper},
        h('input', {
          type: 'text',
          id: forID,
          className: classNameWrapper,
          value: value ? value.get('title') : '',
          onChange: e => onChange({title: e.target.value}),
        }),
        h('button', {
          className: 'btn',
          onClick: this.handleGenerate
        }, 'Generate AI Content')
      );
    }
  });
  
  CMS.registerWidget('ai-content', AIContentWidget);