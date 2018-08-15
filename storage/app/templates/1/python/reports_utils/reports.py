def data(scenarios,stages):
    
    import pickle
    dict_charts = pickle.load( open( "savedata/html_save.p", "rb" ) )
    dict_data = pickle.load( open( "savedata/data_save.p", "rb" ) )
    
    import plotly
    import plotly.graph_objs as go
    
    genHFinal = dict_charts['genHFinal']
    genTFinal = dict_charts['genTFinal']
    genWFinal = dict_charts['genWFinal']
    genDFinal = dict_charts['genDFinal']
    genBFinal = dict_charts['genBFinal']
    horizon = dict_data["horizon"]
    numAreas = dict_data["numAreas"]
    volData = dict_data["volData"]
    thermalData = dict_data["thermalData"]
    battData = dict_data["battData"]
    
    import datetime
    axisfixlow = horizon[0] + datetime.timedelta(hours = -360)
    axisfixhig = horizon[stages-1] + datetime.timedelta(hours = 360)
    x=horizon#list(range(1,stages+1))
    
    ###########################################################################
    
    # all areas dispatch
    dict_fig ={}
    for z in range(numAreas):
        
        y0_org = []
        for j in range(stages):
            val_scn = 0
            for i in range(scenarios):
                val_scn += genWFinal[j][z][i]
            y0_org.append(val_scn/scenarios)
            
        y1_org = []
        for j in range(stages):
            val_stg = 0
            for k in range(len(genHFinal[j])):
                val_scn = 0
                if volData[11][k] == z+1:
                    for i in range(scenarios):
                        val_scn += genHFinal[j][k][i]
                val_stg += val_scn/scenarios
            y1_org.append(val_stg)
        
        y2_org = []
        for j in range(stages):
            val_stg = 0
            for k in range(len(genBFinal[j])):
                val_scn = 0
                if battData[9][k] == z+1:
                    for i in range(scenarios):
                        val_scn += genBFinal[j][k][i]
                val_stg += val_scn/scenarios
            y2_org.append(val_stg)               
        
        y3_org = []
        for j in range(stages):
            val_stg = 0
            for k in range(len(genTFinal[j])):
                val_scn = 0
                if thermalData[3][k] == z+1:
                    for i in range(scenarios):
                        val_scn += genTFinal[j][k][i]
                val_stg += val_scn/scenarios
            y3_org.append(val_stg)
    
        y4_org = []
        for j in range(stages):
            val_scn = 0
            for i in range(scenarios):
                val_scn += genDFinal[j][z][i]
            y4_org.append(val_scn/scenarios)
               
        # Add data to create cumulative stacked values
        y0_stck=y0_org
        y1_stck=[y0+y1 for y0, y1 in zip(y0_org, y1_org)]
        y3_stck=[y0+y1+y3 for y0, y1, y3 in zip(y0_org, y1_org, y3_org)]
        y2_stck=[y0+y1+y3+y2 for y0, y1, y3, y2 in zip(y0_org, y1_org, y3_org, y2_org)]
        y4_stck=[y0+y1+y3+y2+y4 for y0, y1, y3, y2,y4 in zip(y0_org, y1_org, y3_org, y2_org, y4_org)]
        
        # Make original values strings and add % for hover text
        y0_txt=[str("{0:.0f}".format(y0/1000))+' GWh' for y0 in y0_org]
        y1_txt=[str("{0:.0f}".format(y1/1000))+' GWh' for y1 in y1_org]
        y2_txt=[str("{0:.0f}".format(y2/1000))+' GWh' for y2 in y2_org]
        y3_txt=[str("{0:.0f}".format(y3/1000))+' GWh' for y3 in y3_org]
        y4_txt=[str("{0:.0f}".format(y4/1000))+' GWh' for y4 in y4_org]
        
        Wind = go.Scatter(
            x=x,
            y=y0_stck,
            text=y0_txt,
            hoverinfo='x+text',
            mode='lines',
            line=dict(width=0.5,
                      color='rgb(224,243,248)'),
            fill='tonexty',
            name='Wind'
        )
        Hydro = go.Scatter(
            x=x,
            y=y1_stck,
            text=y1_txt,
            hoverinfo='x+text',
            mode='lines',
            line=dict(width=0.5,
                      color='rgb(69,117,180)'),
            fill='tonexty',
            name='Hydro'
        )
        Thermal = go.Scatter(
            x=x,
            y=y3_stck,
            text=y3_txt,
            hoverinfo='x+text',
            mode='lines',
            line=dict(width=0.5,
                      color='rgb(215,48,39)'),
            fill='tonexty',
            name='Thermal'
        )
        Batteries = go.Scatter(
            x=x,
            y=y2_stck,
            text=y2_txt,
            hoverinfo='x+text',
            mode='lines',
            line=dict(width=0.5,
                      color='rgb(111, 231, 219)'),
            fill='tonexty',
            name='Batteries'
        )
        Deficit = go.Scatter(
            x=x,
            y=y4_stck,
            text=y4_txt,
            hoverinfo='x+text',
            mode='lines',
            line=dict(width=0.5,),
                      #color='rgb(131, 90, 241)'),
            fill='tonexty',
            name='Deficit'
        )
        data = [Wind, Hydro, Thermal, Batteries, Deficit]
        layout = go.Layout(
        autosize=False,
        width=800,
        height=500,
        #title='Double Y Axis Example',
        yaxis=dict(title='Energy [MWh]',
                   titlefont=dict(
                           family='Arial, sans-serif',
                           size=18,
                           color='darkgrey'),
                   #tickformat = ".0f"
                   exponentformat = "e",
                   #showexponent = "none",
                   ticks = "inside"
                   ),
        xaxis=dict(range=[axisfixlow,axisfixhig])
        )
        #layout = go.Layout(showlegend=False)
        fig = go.Figure(data=data, layout=layout)
        # plotly.offline.plot(fig, filename='stacked-area-plot-hover', output_type = 'div')
        dict_fig["string{0}".format(z+1)] = plotly.offline.plot(fig, output_type = 'div')
        
    ###########################################################################
    
    # each areas dispatch
    y0_org = []
    for j in range(stages):
        val_stg = 0
        for k in range(len(genWFinal[j])):
            val_scn = 0
            for i in range(scenarios):
                val_scn += genWFinal[j][k][i]
            val_stg += val_scn/scenarios
        y0_org.append(val_stg)
        
    y1_org = []
    for j in range(stages):
        val_stg = 0
        for k in range(len(genHFinal[j])):
            val_scn = 0
            for i in range(scenarios):
                val_scn += genHFinal[j][k][i]
            val_stg += val_scn/scenarios
        y1_org.append(val_stg)
    
    y2_org = []
    for j in range(stages):
        val_stg = 0
        for k in range(len(genBFinal[j])):
            val_scn = 0
            for i in range(scenarios):
                val_scn += genBFinal[j][k][i]
            val_stg += val_scn/scenarios
        y2_org.append(val_stg)               
    
    y3_org = []
    for j in range(stages):
        val_stg = 0
        for k in range(len(genTFinal[j])):
            val_scn = 0
            for i in range(scenarios):
                val_scn += genTFinal[j][k][i]
            val_stg += val_scn/scenarios
        y3_org.append(val_stg)

    y4_org = []
    for j in range(stages):
        val_stg = 0
        for k in range(len(genDFinal[j])):
            val_scn = 0
            for i in range(scenarios):
                val_scn += genDFinal[j][k][i]
            val_stg += val_scn/scenarios
        y4_org.append(val_stg)
           
    # Add data to create cumulative stacked values
    y0_stck=y0_org
    y1_stck=[y0+y1 for y0, y1 in zip(y0_org, y1_org)]
    y3_stck=[y0+y1+y3 for y0, y1, y3 in zip(y0_org, y1_org, y3_org)]
    y2_stck=[y0+y1+y3+y2 for y0, y1, y3, y2 in zip(y0_org, y1_org, y3_org, y2_org)]
    y4_stck=[y0+y1+y3+y2+y4 for y0, y1, y3, y2,y4 in zip(y0_org, y1_org, y3_org, y2_org, y4_org)]
    
    # Make original values strings and add % for hover text
    y0_txt=[str("{0:.0f}".format(y0/1000))+' GWh' for y0 in y0_org]
    y1_txt=[str("{0:.0f}".format(y1/1000))+' GWh' for y1 in y1_org]
    y2_txt=[str("{0:.0f}".format(y2/1000))+' GWh' for y2 in y2_org]
    y3_txt=[str("{0:.0f}".format(y3/1000))+' GWh' for y3 in y3_org]
    y4_txt=[str("{0:.0f}".format(y4/1000))+' GWh' for y4 in y4_org]
    
    Wind = go.Scatter(
        x=x,
        y=y0_stck,
        text=y0_txt,
        hoverinfo='x+text',
        mode='lines',
        line=dict(width=0.5,
                  color='rgb(224,243,248)'),
        fill='tonexty',
        name='Wind'
    )
    Hydro = go.Scatter(
        x=x,
        y=y1_stck,
        text=y1_txt,
        hoverinfo='x+text',
        mode='lines',
        line=dict(width=0.5,
                  color='rgb(69,117,180)'),
        fill='tonexty',
        name='Hydro'
    )
    Thermal = go.Scatter(
        x=x,
        y=y3_stck,
        text=y3_txt,
        hoverinfo='x+text',
        mode='lines',
        line=dict(width=0.5,
                  color='rgb(215,48,39)'),
        fill='tonexty',
        name='Thermal'
    )
    Batteries = go.Scatter(
        x=x,
        y=y2_stck,
        text=y2_txt,
        hoverinfo='x+text',
        mode='lines',
        line=dict(width=0.5,
                  color='rgb(111, 231, 219)'),
        fill='tonexty',
        name='Batteries'
    )
    Deficit = go.Scatter(
        x=x,
        y=y4_stck,
        text=y4_txt,
        hoverinfo='x+text',
        mode='lines',
        line=dict(width=0.5,),
                  #color='rgb(131, 90, 241)'),
        fill='tonexty',
        name='Deficit'
    )
    data = [Wind, Hydro, Thermal, Batteries, Deficit]
    layout = go.Layout(
    autosize=False,
    width=800,
    height=500,
    #title='Double Y Axis Example',
    yaxis=dict(title='Energy [MWh]',
               titlefont=dict(
                       family='Arial, sans-serif',
                       size=18,
                       color='darkgrey'),
               #tickformat = ".0f"
               exponentformat = "e",
               #showexponent = "none",
               ticks = "inside"
               ),
    xaxis=dict(range=[axisfixlow,axisfixhig])
    )
    #layout = go.Layout(showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    # plotly.offline.plot(fig, filename='stacked-area-plot-hover', output_type = 'div')
    graf3 = plotly.offline.plot(fig, output_type = 'div')
    
    ###########################################################################
    
    from jinja2 import Environment, FileSystemLoader
    
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("template_report.html")
    
    template_vars = {"title" : "Report",
                     "data1": "Each area dispatch",
                     "div_placeholder1A": dict_fig["string1"],
                     "div_placeholder1B": dict_fig["string2"],
                     "div_placeholder1C": dict_fig["string3"],
                     "div_placeholder1D": dict_fig["string4"],
                     "div_placeholder1E": dict_fig["string5"],
                     "data2": "All areas",
                     "div_placeholder2": graf3,
                     #"data3": ,
                     #"div_placeholder3": ,
                     #"data4": ,
                     #"div_placeholder4": 
                     }
    
    html_out = template.render(template_vars)
    
    Html_file= open("results/results_report.html","w")
    Html_file.write(html_out)
    Html_file.close()