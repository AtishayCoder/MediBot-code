def micro(time, pos_list):
    for i in pos_list:
        # Fever
        if str(i[0]).lower() == "fever" or str(i[0]).lower() == "temperature":
            if (str(list(time)[-1]).lower() == "m" or str(list(time)[-1]).lower() == "y" or str(
                    list(time)[-1]).lower() == "w") or (int(list(time)[0]) > 7 and str(list(time)[-1]).lower() == "d"):
                # Chronic disease
                for _ in pos_list:
                    # HIV
                    if _[0].lower() == "swelling":
                        for a in pos_list:
                            if a[0].lower() == "shoulder" or a[0].lower() == "hips" or a[0].lower() == "butt" or a[
                                0].lower() == "buttocks" or a[0].lower() == "neck" or a[0].lower() == "chest":
                                return "result/The diagnosis is HIV."
                    # Tuberculosis
                    elif _[0].lower() == "night":
                        for z in pos_list:
                            if z[0].lower() == "sweating" or z[0].lower() == "sweats" or z[0].lower() == "sweat":
                                return "result/The diagnosis is Tuberculosis."
                    # Malnutrition
                    elif _[0].lower() == "growth":
                        for y in pos_list:
                            if y[0].lower() == "stunted" or y[0].lower() == "low" or y[0].lower() == "less":
                                return "result/The diagnosis is Malnutrition."
                    # Chronic infection
                    elif _[0].lower() == "weight":
                        for x in pos_list:
                            if x[0].lower() == "low" or x[0].lower() == "less" or x[0].lower() == "decreasing":
                                return "result/The diagnosis is Chronic Infection."

            elif int(list(time)[0]) <= 7 and str(list(time)[-1]).lower() == "d":
                # Acute disease
                for b in pos_list:
                    # Malaria
                    if b[0].lower() == "cold" or b[0].lower() == "cool" or b[0].lower() == "chills" or b[0].lower() == "chill":return "result/The diagnosis is Malaria."
                    # Typhoid
                    elif b[0].lower() == "hunger" or b[0].lower() == "stomach" or b[0].lower() == "eating" or b[0].lower() == "eat" or b[0].lower() == "food":
                        for c in pos_list:
                            if c[0].lower() == "no" or c[0].lower() == "less" or c[0].lower() == "full" or c[0].lower() == "feel":
                                return "result/The result is Typhoid."
                    # Dengue
                    elif b[0].lower() == "nose":
                        for d in pos_list:
                            if d[0].lower() == "bleeding" or d[0].lower() == "bleed" or d[0].lower() == "bleeds" or d[
                                0].lower() == "blood":
                                return "result/The diagnosis is Dengue."
                    # Viral infection
                    elif b[0].lower() == "cough" or b[0].lower() == "nose":
                        for e in pos_list:
                            if e[0].lower() == "running" or e[0].lower() == "runny" or e[0].lower() == "mucus":
                                return "result/The diagnosis is Viral Infection."
                    # Bacterial infection
                    elif b[0].lower() == "pain":
                        for f in pos_list:
                            if f[0].lower() == "area" or f[0].lower() == "certain" or f[0].lower() == "one" or f[0].lower() == "place":
                                return "result/The diagnosis is Bacterial Infection."
        # Respiratory
        elif str(i[0]).lower() == "cough" or str(i[0]).lower() == "coughing":
            for g in pos_list:
                # Pneumonia (Productive cough)
                if g[0].lower() == "mucus" or g[0].lower() == "liquid":
                    for h in pos_list:
                        if h[0].lower() == "chest":
                            for _ in pos_list:
                                if _[0].lower() == "pain":
                                    return "result/The diagnosis is Pneumonia."
                # Dry cough
                elif g[0].lower() == "dried" or g[0].lower() == "dry":
                    for h in pos_list:
                        # Asthma
                        if h[0].lower() == "chest":
                            for j in pos_list:
                                if j[0].lower() == "tightness" or j[0].lower() == "tight" or j[0].lower() == "pressure" or j[0].lower() == "ripping" or j[0].lower() == "rip":
                                    return "result/The diagnosis is Asthma."
                        # Bronchitis
                        elif h[0].lower() == "breath" or "gasp":
                            for k in pos_list:
                                if k[0].lower() == "shortness" or k[0].lower() == "problem" or k[0].lower() == "difficulty" or k[0].lower() == "difficult":
                                    return "result/The diagnosis is Bronchitis."
        # Heart attack
        elif str(i[0]).lower() == "breath" or str(i[0]).lower() == "gasp":
            for l in pos_list:
                if l[0].lower() == "shortness" or l[0].lower() == "problem" or l[0].lower() == "difficulty" or l[0].lower() == "difficult":
                    for m in pos_list:
                        if m[0].lower() == "swelling" or m[0].lower() == "swell" or m[0].lower() == "sphere" or m[0].lower() == "circle":
                            pass
