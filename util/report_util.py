from util.config_uti import Configuration

class Report_Utility():
    Error_Title = None

    def __init__(self):
        pass
    
    async def analysis_table(self, issues, suggestions, percentage):
        html = ""
        if issues:
            html_template = """<div class="module" id="cookies">
                                <h2>""" + Configuration.MODULE_COOKIES + """&nbsp; Score = """ + str(percentage) + """%</h2>
                                <div style="display: inline; font-weight: bold;">Summary :</div>
                                <span style="display: inline;">The """ + Configuration.MODULE_COOKIES + """ used on the website meet most security standards. However, there are a couple of issues that need to be addressed.</span>
                                <div class="issues">
                                    <h4>Identified Issues:</h4>
                                    <ul>
                                        {issue_items}
                                    </ul>
                                </div>
                                <div class="suggestions">
                                    <h4>Suggestions for Improvement:</h4>
                                    <ul>
                                        {suggestion_items}
                                    </ul>
                                </div> 
                        </div>"""

            # Generate the list items for issues and suggestions
            issue_items = ''.join([f"<li>{issue}</li>" for issue in issues])
            suggestion_items = ''.join([f"<li>{suggestion}</li>" for suggestion in suggestions])

            # Insert the list items into the HTML template
            html = html_template.format(issue_items=issue_items, suggestion_items=suggestion_items)
        return html
