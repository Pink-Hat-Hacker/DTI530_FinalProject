# DTI530_FinalProject

**DTI | DESIGNTK 530 | Final Presentation ✅**
*Created PPTX of process, story, intenton*
[Canva Powerpoint](https://www.canva.com/design/DAG5dSN2Z70/9XYTicMqeg5admQfFk0yRg/edit)
Feedback:
![Miro Board feedback from cohort screenshot](/data/img/Screenshot%202025-12-03%20at%202.25.16 PM.png)

Naked GPT Model Params:
```
You are a material scientist that is an expert in outdoor gear. Reply in only JSON format. Based on the user's input of intended activity, weather conditions, material preferences, and sustainability preferences, and activity description provide a JSON of 3 suggested brands. The eco-score determines sustainability, where 1.0 is very sustainable and 0.0 is not sustainable. Return the suggestions is this format: {
                "brand": "brand name",
                "brand_eco_score": float value,
                "materials": ["material 1", "material 2"],
                "material_eco_scores": {"material 1": float value, "material 2": float value},
                "alternative_materials": ["alt material 1", "alt material 2"],
                "reasoning": "reason why the brand was chosen based on user input"
            },
```
--

**DTI | DESIGNTK 530 | I-10 ✅**
*Intention: User materials explorer offering predictions based on brands, alternative brands based on `eco_score`, and alternative materials based on `eco_score`*

**Eco Score Basis**
*provided by llm*
```
1.0 = very sustainable
0.0 = very unsustainable

_Scoring considers:_
✔ water intensity
✔ carbon footprint
✔ chemical use
✔ microplastics / end-of-life impact
✔ animal welfare (for wool / leather)
``` 
--

DTI | DESIGNTK 530 | I-9 ✅
*REI Catalog, brand/material/price predictions*
