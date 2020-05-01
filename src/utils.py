import numpy as np

base_note = 68
base_freq = 440*2**((base_note-81)/12)
pbs = 12
N_hanning = 20
bias = 0
max_freq = base_freq * 2**(pbs/12)
min_freq = base_freq * 2**(-pbs/12)
dots_per_beat = 480
tempo = 6000
ms_per_dot = 6000000 / tempo / dots_per_beat
tail_const = '''        </vsPart>
	</vsTrack>
	<monoTrack>
	</monoTrack>
	<stTrack>
	</stTrack>
	<aux>
		<id><![CDATA[AUX_VST_HOST_CHUNK_INFO]]></id>
		<content><![CDATA[VlNDSwAAAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=]]></content>
	</aux>
</vsq4>
'''
def write_head(file, tot_time = 10000):
    tot_dots = int(tot_time * 6.0 / tempo *dots_per_beat)
    head_const = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<vsq4 xmlns="http://www.yamaha.co.jp/vocaloid/schema/vsq4/"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://www.yamaha.co.jp/vocaloid/schema/vsq4/ vsq4.xsd">
	<vender><![CDATA[Yamaha corporation]]></vender>
	<version><![CDATA[4.0.0.3]]></version>
	<vVoiceTable>
		<vVoice>
			<bs>4</bs>
			<pc>0</pc>
			<id><![CDATA[BE8A88G3FWXLTEBD]]></id>
			<name><![CDATA[YuezhenglingV3]]></name>
			<vPrm>
				<bre>0</bre>
				<bri>0</bri>
				<cle>0</cle>
				<gen>0</gen>
				<ope>0</ope>
			</vPrm>
		</vVoice>
	</vVoiceTable>
	<mixer>
		<masterUnit>
			<oDev>0</oDev>
			<rLvl>0</rLvl>
			<vol>0</vol>
		</masterUnit>
		<vsUnit>
			<tNo>0</tNo>
			<iGin>0</iGin>
			<sLvl>-898</sLvl>
			<sEnable>0</sEnable>
			<m>0</m>
			<s>0</s>
			<pan>64</pan>
			<vol>0</vol>
		</vsUnit>
		<monoUnit>
			<iGin>0</iGin>
			<sLvl>-898</sLvl>
			<sEnable>0</sEnable>
			<m>0</m>
			<s>0</s>
			<pan>64</pan>
			<vol>0</vol>
		</monoUnit>
		<stUnit>
			<iGin>0</iGin>
			<m>0</m>
			<s>0</s>
			<vol>-129</vol>
		</stUnit>
	</mixer>
	<masterTrack>
		<seqName><![CDATA[Untitled0]]></seqName>
		<comment><![CDATA[New VSQ File]]></comment>
		<resolution>480</resolution>
		<preMeasure>4</preMeasure>
		<timeSig><m>0</m><nu>4</nu><de>4</de></timeSig>
		<tempo><t>0</t><v>'''+str(tempo)+'''</v></tempo>
	</masterTrack>
	<vsTrack>
		<tNo>0</tNo>
		<name><![CDATA[Track]]></name>
		<comment><![CDATA[Track]]></comment>
		<vsPart>
			<t>7680</t>
			<playTime>'''+str(tot_dots)+'''</playTime>
			<name><![CDATA[NewPart]]></name>
			<comment><![CDATA[New Musical Part]]></comment>
			<sPlug>
				<id><![CDATA[ACA9C502-A04B-42b5-B2EB-5CEA36D16FCE]]></id>
				<name><![CDATA[VOCALOID2 Compatible Style]]></name>
				<version><![CDATA[3.0.0.1]]></version>
			</sPlug>
			<pStyle>
				<v id="accent">50</v>
				<v id="bendDep">8</v>
				<v id="bendLen">0</v>
				<v id="decay">50</v>
				<v id="fallPort">0</v>
				<v id="opening">127</v>
				<v id="risePort">0</v>
			</pStyle>
			<singer>
				<t>0</t>
				<bs>4</bs>
				<pc>0</pc>
			</singer>
'''
    file.write(head_const)

def write_tail(file):
    file.write(tail_const)

def write_pit(file, f0, t):
    file.write('\t\t\t<cc><t>1</t><v id="S">'+str(pbs)+'</v></cc>\n')
    f0 = np.log2((f0+0.001) / 440.0) * 12 + 81
    t = t * 1000
    t = t / ms_per_dot + dots_per_beat
    for i in range(len(t)):
        t[i] = int(t[i]+0.5)
        if f0[i] < 0:
            pit_ = 0
        else:
            pit_ = int((f0[i] - base_note) / pbs * 8192+0.5)
            if pit_ > 8191:
                pit_ = 8191
            elif pit_ < -8192:
                pit_ = -8192
        f0[i] = pit_

    hn_weights = np.hanning(N_hanning)
    f0_s = np.convolve(hn_weights/hn_weights.sum(),f0)[N_hanning-1:-N_hanning+1]
    t = t[N_hanning - 1:]
    for i in range(len(t)):
        file.write('\t\t\t<cc><t>'+str(int(t[i]))+'</t><v id="P">'+str(int(f0_s[i]+0.5))+'</v></cc>\n')

def write_note(file, infile):
    for i in range(14):
        line = infile.readline()
    while line:
        line = infile.readline()
        if not line:
            break
        xmin = int(float(infile.readline().split()[-1]) *1000/ ms_per_dot + 0.5) + N_hanning - 1 + dots_per_beat + bias
        xmax = int(float(infile.readline().split()[-1]) *1000/ ms_per_dot + 0.5) + N_hanning - 1 + dots_per_beat + bias
        note = infile.readline().split()[-1][1:-1]
        dur = xmax - xmin
        if not note:
            continue
        file.write('\t\t\t<note>\n\t\t\t\t<t>'+str(xmin)+'</t>\n\t\t\t\t<dur>'+str(dur)+'</dur>\n\t\t\t\t<n>'+str(base_note) \
            +'</n>\n\t\t\t\t<v>64</v>\n\t\t\t\t<y><![CDATA['+note+']]></y>\n\t\t\t\t<p><![CDATA[a]]></p>\n')
        file.write('''				<nStyle>
					<v id="accent">50</v>
					<v id="bendDep">0</v>
					<v id="bendLen">0</v>
					<v id="decay">50</v>
					<v id="fallPort">0</v>
					<v id="opening">127</v>
					<v id="risePort">0</v>
					<v id="vibLen">0</v>
					<v id="vibType">0</v>
				</nStyle>
			</note>
''')