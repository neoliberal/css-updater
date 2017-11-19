 1. Read Secrets from secrets.json
 
 2. Start Flask Server
 
 3. Listen to Webhooks
    * Authenticate that webhook is authentic by comparing hashes
    * Take the webhook data and pass it into a Holder Object
   
 4. Using data gathered from Webhook, Clone Repo
    * Determine if push is Test or Master [based on branch]
    * Use Tempdirs for security purposes
    * Read internal Config file
 
 5. Compile Repo
    * Detect if SASS or CSS
    * Perform pre_push functions to transform codebase
    * Hook custom functions into compile (if SASS)
    * Get CSS
      * Minify / Compress
    
  6. Push to Reddit
    * Push Stylesheet
    * Push Images and if they changed
    * Read any errors and pipe them back to either Slack / Modmail
