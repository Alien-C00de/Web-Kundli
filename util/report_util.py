from util.config_uti import Configuration

class Report_Utility():
    Error_Title = None

    def __init__(self):
        pass
    
    async def analysis_table(self, icone, module_name, issues, suggestions, percentage):
        html = ""
        if issues:
            html_template ="""
                    <div class="section cookies">
                        <h2><i class=""" + icone + """></i>&nbsp;&nbsp;&nbsp;""" + module_name + """&nbsp; Score = """ + str(percentage) + """%</h2>
                        <p><strong>Summary:</strong> The """ + module_name + """ used on the website meet most security standards, but some issues need attention.</p>
                        <div class="issues">
                            <h3>Identified Issues:</h3>
                            <ul>
                                {issue_items}
                            </ul>
                        </div>
                        <div class="suggestions">
                            <h3>Suggestions for Improvement:</h3>
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
    

    async def Empty_Table(self, warning = "", percentage = 0):
        table = f"""<table>
                        <tr>
                            <td colspan="2">
                                <div class="progress-bar-container">
                                    <div class="progress" style="width: {str(percentage)}%;">{str(percentage)}%</div>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td colspan="2" style="text-align: left;">{warning}</td>
                        </tr>
                        <tr>
                    </table>"""
        return table