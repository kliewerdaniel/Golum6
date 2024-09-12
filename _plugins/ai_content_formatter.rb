module Jekyll
    class AIContentFormatter
      def self.format(site, page)
        return unless page['ai_content']
  
        title = page['ai_content']['title']
        content = page['ai_content']['body']
        comments = page['ai_content']['ai_comments']
  
        formatted_content = <<~CONTENT
          ---
          layout: post
          title: "#{title}"
          date: #{Time.now.strftime('%Y-%m-%d %H:%M:%S %z')}
          categories: []
          ---
  
          #{content}
  
          ## AI-Generated Comments
          #{comments}
        CONTENT
  
        page.content = formatted_content
      end
    end
  
    class AIContentGenerator < Generator
      def generate(site)
        site.pages.each do |page|
          AIContentFormatter.format(site, page)
        end
      end
    end
  end