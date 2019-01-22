# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2016, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

# This uses plotly to create a nice looking graph of average false positive
# error rates as a function of N, the dimensionality of the vectors.  I'm sorry
# this code is so ugly.

import plotly.plotly as py
import plotly.graph_objs as go
import os

plotlyUser = os.environ['PLOTLY_USERNAME']
plotlyAPIKey = os.environ['PLOTLY_API_KEY']


py.sign_in(plotlyUser, plotlyAPIKey)


# Calculated error values

# a=64 cells active, s=24 synapses on segment, dendritic threshold is theta=12
errorsA64 = [0.00109461662333690, 5.69571108769533e-6, 1.41253230930730e-7,
8.30107183322324e-9, 8.36246969414003e-10, 1.21653747887184e-10,
2.30980246348674e-11, 5.36606800342786e-12, 1.46020443491340e-12,
4.51268292560082e-13, 1.54840085336688e-13, 5.79872960230082e-14,
2.33904818374099e-14, 1.00570025123595e-14, 4.57067109837325e-15,
2.18074665975532e-15, 1.08615761649705e-15, 5.62075747510851e-16,
3.01011222991216e-16, 1.66258638217391e-16, 9.44355122475050e-17,
5.50227860973758e-17, 3.28135862312369e-17, 1.99909942419741e-17,
1.24208005365401e-17, 7.85865625150437e-18, 5.05651456769333e-18,
3.30476684404715e-18, 2.19155538525467e-18, 1.47322040125054e-18,
1.00301732527126e-18, 6.91085187713756e-19, 4.81531998098323e-19,
3.39081789745300e-19, 2.41162129140343e-19, 1.73141122432297e-19,
1.25417524780710e-19, 9.16179854408830e-20, 6.74653665117861e-20,
5.00594093406879e-20, 3.74140647385797e-20, 2.81565500298724e-20,
2.13295032637269e-20, 1.62595896290270e-20, 1.24693930357791e-20,
9.61778646245879e-21, 7.45921945784706e-21, 5.81568673720061e-21,
4.55727209094172e-21, 3.58853982726974e-21, 2.83894572073852e-21,
2.25603220132537e-21, 1.80056639958786e-21, 1.44304355442520e-21,
1.16115649370912e-21, 9.37953155574248e-22, 7.60487232154203e-22,
6.18824388817498e-22, 5.05306382976791e-22, 4.14003297073025e-22,
3.40303733585598e-22, 2.80606724840170e-22, 2.32089016319463e-22,
1.92528479384963e-22, 1.60169522159935e-22, 1.33620070237719e-22,
1.11772384488816e-22, 9.37419553557710e-23, 7.88201628070397e-23,
6.64374619109495e-23, 5.61346484579118e-23, 4.75403511103980e-23,
4.03533396572869e-23, 3.43285719468893e-23, 2.92661533398441e-23,
2.50025728639646e-23, 2.14037249918740e-23, 1.83593364333338e-23,
1.57785019555348e-23, 1.35860982932100e-23, 1.17198953848347e-23,
1.01282230018514e-23, 8.76808098727516e-24, 7.60360480333303e-24,
6.60481643546819e-24, 5.74660507849120e-24, 5.00789333176087e-24,
4.37095353819125e-24, 3.82084594311781e-24, 3.34495593004021e-24,
2.93261202567532e-24, 2.57476990096962e-24, 2.26375041804855e-24,
1.99302203415240e-24, 1.75701968882530e-24, 1.55099376138908e-24,
1.37088386401156e-24, 1.21321318827475e-24, 1.07499989501613e-24]

# a=128 cells active, s=24 synapses on segment, dendritic threshold is theta=12
errorsA128 = [0.292078213737764, 0.00736788303358289, 0.000320106080889471,
2.50255519815378e-5, 2.99642102590114e-6, 4.89399786076359e-7,
1.00958512780931e-7, 2.49639031779358e-8, 7.13143762262004e-9,
2.29143708340810e-9, 8.11722283609541e-10, 3.12183638427824e-10,
1.28795248562774e-10, 5.64573534731427e-11, 2.60920666735517e-11,
1.26329222640928e-11, 6.37403647747254e-12, 3.33669667244209e-12,
1.80542698201560e-12, 1.00649239071800e-12, 5.76511433714795e-13,
3.38478276365079e-13, 2.03268423835688e-13, 1.24631220425762e-13,
7.78926809872514e-14, 4.95511644935965e-14, 3.20435767306233e-14,
2.10406420101461e-14, 1.40139130251568e-14, 9.45883828128567e-15,
6.46439769450458e-15, 4.46990041341270e-15, 3.12495999111406e-15,
2.20745309613471e-15, 1.57465638743741e-15, 1.13369191106350e-15,
8.23389688886499e-16, 6.03003384235568e-16, 4.45098155251971e-16,
3.31012812127460e-16, 2.47930640620987e-16, 1.86967641684828e-16,
1.41911643042882e-16, 1.08382344694871e-16, 8.32664249878792e-17,
6.43341686630739e-17, 4.99770213701060e-17, 3.90264314839685e-17,
3.06278060677719e-17, 2.41521444354171e-17, 1.91336334608186e-17,
1.52252678771373e-17, 1.21670765082745e-17, 9.76322639206603e-18,
7.86542142828590e-18, 6.36079286593057e-18, 5.16301523572075e-18,
4.20575231020497e-18, 3.43779601881797e-18, 2.81944231990508e-18,
2.31977574047117e-18, 1.91462490842612e-18, 1.58501607064100e-18,
1.31599800204033e-18, 1.09574520166929e-18, 9.14870565820523e-19,
7.65896441163367e-19, 6.42845939069147e-19, 5.40925947054799e-19,
4.56280340219040e-19, 3.85797146007365e-19, 3.26957333574643e-19,
2.77715835010627e-19, 2.36407614922344e-19, 2.01673273889071e-19,
1.72399937123611e-19, 1.47674143329993e-19, 1.26744185074274e-19,
1.08989916627431e-19, 9.38984797396823e-20, 8.10447332969045e-20,
7.00754327115433e-20, 6.06964068938479e-20, 5.26621381311802e-20,
4.57672733591788e-20, 3.98396919091576e-20, 3.47348308088003e-20,
3.03310286648971e-20, 2.65256965853905e-20, 2.32321622214084e-20,
2.03770629346944e-20, 1.78981879590753e-20, 1.57426885025016e-20,
1.38655900262325e-20, 1.22285532217681e-20, 1.07988400985754e-20,
9.54844958066234e-21, 8.45339347007471e-21, 7.49308887332261e-21]

# a=256 cells active, s=24 synapses on segment, dendritic threshold is theta=12
errorsA256 = [0.999997973443107, 0.629372754740777, 0.121087724790945,
0.0193597645959856, 0.00350549721741729, 0.000748965962032781,
0.000186510373919969, 5.30069204544174e-5, 1.68542688790000e-5,
5.89560747849969e-6, 2.23767020178735e-6, 9.11225564771580e-7,
3.94475072403605e-7, 1.80169987461924e-7, 8.62734957588259e-8,
4.30835081022293e-8, 2.23380881095835e-8, 1.19793311140766e-8,
6.62301584036177e-9, 3.76438169312996e-9, 2.19423953869126e-9,
1.30887557403056e-9, 7.97480990380968e-10, 4.95482969325862e-10,
3.13460830324406e-10, 2.01656908833009e-10, 1.31767135541276e-10,
8.73586539716713e-11, 5.87077297245969e-11, 3.99576761200323e-11,
2.75220232248960e-11, 1.91701608847159e-11, 1.34943954043346e-11,
9.59410134279997e-12, 6.88558106762690e-12, 4.98590018053347e-12,
3.64092373686549e-12, 2.68014488783288e-12, 1.98797603387229e-12,
1.48528633835993e-12, 1.11739495331362e-12, 8.46179085322245e-13,
6.44833912395788e-13, 4.94359544385977e-13, 3.81184046390743e-13,
2.95540942533515e-13, 2.30352375229645e-13, 1.80454125570680e-13,
1.42053695445942e-13, 1.12348554361008e-13, 8.92553023993497e-14,
7.12162118182915e-14, 5.70601336962939e-14, 4.59018613132802e-14,
3.70688756443847e-14, 3.00477108050374e-14, 2.44444632746040e-14,
1.99555570507925e-14, 1.63459876978165e-14, 1.34330500162347e-14,
1.10741076071588e-14, 9.15735686079334e-15, 7.59482030375183e-15,
6.31700763775213e-15, 5.26883007721797e-15, 4.40646078058260e-15,
3.69491257084125e-15, 3.10616176350258e-15, 2.61768946987837e-15,
2.21134330625883e-15, 1.87244595538993e-15, 1.58909462235613e-15,
1.35160864769231e-15, 1.15209251425918e-15, 9.84089038159454e-16,
8.42303276784589e-16, 7.22382069351279e-16, 6.20737481445016e-16,
5.34405004455211e-16, 4.60929349954820e-16, 3.98272218221725e-16,
3.44737614911305e-16, 2.98911220348303e-16, 2.59611042743928e-16,
2.25847156136861e-16, 1.96788771381788e-16, 1.71737241200100e-16,
1.50103879041435e-16, 1.31391692394609e-16, 1.15180306705465e-16,
1.01113495891954e-16, 8.88888471340935e-17, 7.82491770468619e-17,
6.89753881281890e-17, 6.08805121319100e-17, 5.38047335965072e-17,
4.76112244136112e-17, 4.21826508250283e-17, 3.74182390049037e-17]

# a=n/2 cells active, s=24 synapses on segment, dendritic threshold is theta=12
errorsAHalfOfN = [0.00518604306750049, 0.00595902789913702, 0.00630387009654985,
0.00649883841432922, 0.00662414645898081, 0.00671145554136860,
0.00677576979476038, 0.00682511455944402, 0.00686417048273405,
0.00689585128896232, 0.00692206553525732, 0.00694411560202313,
0.00696292062841680, 0.00697914780884254, 0.00699329317658955,
0.00700573317947932, 0.00701675866709042, 0.00702659791060005,
0.00703543257326555, 0.00704340902766207, 0.00705064652812678,
0.00705724321275902, 0.00706328057895142, 0.00706882686694759,
0.00707393965010535, 0.00707866784069150, 0.00708305325948833,
0.00708713187600340, 0.00709093479720398, 0.00709448906232020,
0.00709781828668885, 0.00710094318706191, 0.00710388201308149,
0.00710665090391040, 0.00710926418473885, 0.00711173461466950,
0.00711407359503532, 0.00711629134532740, 0.00711839705245984,
0.00712039899796979, 0.00712230466686664, 0.00712412084114628,
0.00712585368043317, 0.00712750879177102, 0.00712909129022819,
0.00713060585169798, 0.00713205675904178, 0.00713344794253425,
0.00713478301541479, 0.00713606530522246, 0.00713729788148649,
0.00713848358025748, 0.00713962502589200, 0.00714072465044275,
0.00714178471095577, 0.00714280730493375, 0.00714379438418811,
0.00714474776727266, 0.00714566915066510, 0.00714656011884143,
0.00714742215336873, 0.00714825664112637, 0.00714906488175141,
0.00714984809439242, 0.00715060742384539, 0.00715134394613683,
0.00715205867361116, 0.00715275255957311, 0.00715342650252986,
0.00715408135007252, 0.00715471790243238, 0.00715533691574314,
0.00715593910503720, 0.00715652514700088, 0.00715709568251095,
0.00715765131897250, 0.00715819263247588, 0.00715872016978916,
0.00715923445020018, 0.00715973596722158, 0.00716022519017042,
0.00716070256563302, 0.00716116851882463, 0.00716162345485272,
0.00716206775989168, 0.00716250180227608, 0.00716292593351907,
0.00716334048926185, 0.00716374579015949, 0.00716414214270805,
0.00716452984001762, 0.00716490916253519, 0.00716528037872114,
0.00716564374568296, 0.00716599950976899, 0.00716634790712550,
0.00716668916421930, 0.00716702349832872, 0.00716735111800491]

listofNValues = [300, 500, 700, 900, 1100, 1300, 1500, 1700, 1900, 2100, 2300,
2500, 2700, 2900, 3100, 3300, 3500, 3700, 3900, 4100, 4300, 4500, 4700, 4900,
5100, 5300, 5500, 5700, 5900, 6100, 6300, 6500, 6700, 6900, 7100, 7300, 7500,
7700, 7900, 8100, 8300, 8500, 8700, 8900, 9100, 9300, 9500, 9700, 9900, 10100,
10300, 10500, 10700, 10900, 11100, 11300, 11500, 11700, 11900, 12100, 12300,
12500, 12700, 12900, 13100, 13300, 13500, 13700, 13900, 14100, 14300, 14500,
14700, 14900, 15100, 15300, 15500, 15700, 15900, 16100, 16300, 16500, 16700,
16900, 17100, 17300, 17500, 17700, 17900, 18100, 18300, 18500, 18700, 18900,
19100, 19300, 19500, 19700, 19900]

trace1 = go.Scatter(
    y=errorsA64,
    x=listofNValues,
    line=dict(
        color='rgb(0, 0, 0)',
        width=3,
        shape='spline'
    ),
    name="a=64"
)

trace2 = go.Scatter(
    y=errorsA128,
    x=listofNValues[1:],
    line=dict(
        color='rgb(0, 0, 0)',
        width=3,
        shape='spline'
    ),
    name="a=128"
)

trace3 = go.Scatter(
    y=errorsA256,
    x=listofNValues[1:],
    line=dict(
        color='rgb(0, 0, 0)',
        width=3,
        shape='spline'
    ),
    name="a=256"
)

trace4 = go.Scatter(
    y=errorsAHalfOfN,
    x=listofNValues[1:],
    line=dict(
        color='rgb(0, 0, 0)',
        width=3,
        dash='dash',
        shape='spline',
    ),
    name="a=0.25*N"
)

data = [trace1, trace2, trace3, trace4]

layout = go.Layout(
    title='',
    showlegend=False,
    autosize=False,
    width=855,
    height=700,
    xaxis=dict(
        title='Vector length (n)',
        titlefont=dict(
            family='Arial',
            size=26,
            color='rgb(0, 0, 0)',
        ),
        tickfont=dict(
            family='Arial',
            size=16,
            color='rgb(0, 0, 0)',
        ),
        exponentformat="none",
        dtick=1000,
        showline=True,
        range=[0, 10000],
    ),
    yaxis=dict(
        title='Probability of false positives',
        type='log',
        exponentformat='power',
        autorange=True,
        titlefont=dict(
            family='Arial',
            size=26,
            color='rgb(0, 0, 0)',
        ),
        tickfont=dict(
            family='Arial',
            size=16,
            color='rgb(0, 0, 0)',
        ),
        showline=True,
    ),
    annotations=[
      dict(
            x=2988,
            y=0.1143,
            xref='x',
            yref='paper',
            text='active bits = 64',
            showarrow=False,
            align='center',
            textangle=0,
            borderwidth=1,
            borderpad=1,
            bgcolor='rgba(0, 0, 0, 0)',
            opacity=1
        ),
  ]
    #   dict(
    #         x=17103,
    #         y=0.259,
    #         xref='x',
    #         yref='paper',
    #         text='$a = 128$',
    #         showarrow=False,
    #         # font=dict(
    #         #     family='',
    #         #     size=24,
    #         #     color=''
    #         # ),
    #         align='center',
    #         textangle=0,
    #         # bordercolor='',
    #         borderwidth=1,
    #         borderpad=1,
    #         bgcolor='rgba(0, 0, 0, 0)',
    #         opacity=1
    #     ),
    #   dict(
    #         x=17132,
    #         y=0.411,
    #         xref='x',
    #         yref='paper',
    #         text='$a = 256$',
    #         showarrow=False,
    #         # font=dict(
    #         #     family='',
    #         #     size=24,
    #         #     color=''
    #         # ),
    #         align='center',
    #         textangle=0,
    #         # bordercolor='',
    #         borderwidth=1,
    #         borderpad=1,
    #         bgcolor='rgba(0, 0, 0, 0)',
    #         opacity=1
    #     ),
    #   dict(
    #         x=16845,
    #         y=0.933,
    #         xref='x',
    #         yref='paper',
    #         text="$a = \\frac{n}{2}$",
    #         showarrow=False,
    #         # font=dict(
    #         #     family='',
    #         #     size=24,
    #         #     color=''
    #         # ),
    #         align='center',
    #         textangle=0,
    #         # bordercolor='',
    #         borderwidth=1,
    #         borderpad=1,
    #         bgcolor='rgba(0, 0, 0, 0)',
    #         opacity=1
    #     )
    #   ]
)

fig = go.Figure(data=data, layout=layout)
plot_url = py.plot(fig, auto_open=False)
print "url=",plot_url
figure = py.get_figure(plot_url)
py.image.save_as(figure, 'images/effect_of_n.pdf', scale=4)