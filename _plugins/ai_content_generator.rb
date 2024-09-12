require 'open3'

module Jekyll
  class AIContentGenerator < Generator
    def generate(site)
      site.posts.docs.each do |post|
        next if post.data['ai_enhanced']

        # Generate AI comments
        comments = generate_ai_comments(post.data['title'])
        post.data['ai_comments'] = comments

        # Mark the post as AI-enhanced
        post.data['ai_enhanced'] = true
      end
    end

    private

    def generate_ai_comments(title)
      command = "python ai_content_generator.py \"#{title}\""
      stdout, stderr, status = Open3.capture3(command)
      
      if status.success?
        stdout.strip
      else
        Jekyll.logger.error "Error generating AI comments: #{stderr}"
        ""
      end
    end
  end
end