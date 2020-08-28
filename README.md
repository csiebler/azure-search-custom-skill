# azure-search-custom-skill

This is a simple example for extraction any `regex` from documents in Azure Cognitive Search.

```json
{
    "skills": [
      "[... your existing skills remain here]",
      {
        "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
        "description": "RegEx extraction Skill",
        "uri": "https://[your-function-url-here]",
        "context": "/document/content/*",
        "inputs": [
        {
            "name": "text1",
            "source": "/document/content"
        }
        ],
        "outputs": [
        {
            "name": "matches",
            "targetName": "product_ids"
        }
        ]
      }
  ]
}
```