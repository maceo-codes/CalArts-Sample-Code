import customtkinter as ctk
import tkinter as tk
import pyaudio
import wave
import time
import threading
import matplotlib.pyplot as plt
import numpy as np
import os
import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from pedalboard import *
from pedalboard.io import AudioFile


#Maceo Parker
#CalArts Sample Code 2
#This program opens a GUI in which you can record audio. After you record, more menus appear which allow
#you to manipulate the audio (add effects, Resample, bitcrush, change pitch, and view the waveform).


#INTRUCTIONS:
#After you record your audio, to hear the effects you apply, click Render. This will create a new wav file in the
#project folder. After you render, you can press the play button to listen to the most recent wav file.
#You can repeat this process forever, or record something new without needing to close and reopen the program.


class Ample_Sample:
    def __init__(self):

#Window Settings
        self.window = ctk.CTk()
        self.window.title('Ample Sample')
        self.window.geometry('1000x600')
        self.window.resizable(False, False)
        ctk.set_appearance_mode('dark')

        self.window.columnconfigure((0,1,2,3), weight=1)
        self.window.rowconfigure((0,1,4), weight=1)
        self.window.rowconfigure((2,3), weight=0)

#GUI Ojects
        #Record Button
        self.r = tk.StringVar()
        self.r.set('Click Here to Record')
        self.rec_button = ctk.CTkButton(
            self.window,
            textvariable=self.r,
            font=('Helvetica',32, 'bold'),
            fg_color='#333333',
            text_color='white',
            hover_color='#2e2e2e',
            command=self.click)
        self.rec_button.grid(row=0, column=1, rowspan=2, columnspan= 2, sticky='snew')
        self.switch = False

        #Record Time Display Clock
        self.t = tk.StringVar()
        self.t.set('00:00:00')
        self.clock = ctk.CTkButton(
            self.window,
            text='00:00:00',
            font=('Helvetica', 12, 'bold'),
            fg_color='#333333',
            text_color='white',
            hover_color='#333333')
        self.clock.grid(row=2, column=1, columnspan=2, sticky='nsew')

        #Button opens matplotlib view of waveform, shows current .wav file name
        self.open_button = ctk.CTkButton(
            self.window,
            text='Open Waveform',
            font=('Helvetica', 18, 'bold'),
            fg_color='transparent',
            command=self.open)

        #Play and Stop Button using Pygame.mixer
        self.play_button = ctk.CTkButton(
            self.window,
            text='▶',
            font=('Century Gothic', 32, 'bold'),
            fg_color='transparent',
            text_color='green',
            command=self.play)

        self.stop_button = ctk.CTkButton(
            self.window,
            text='⏹',
            font=('Century Gothic', 32, 'bold'),
            fg_color='transparent',
            text_color='blue',
            command=self.restart)

    #Tabview of effects from Spotify's Pedalboard Library

        #initializing effect parameter variables
        self.board = ([])
        self.phaseramount=0
        self.chorusamount=0
        self.roomsize=0
        self.distoamount=0
        self.delaytime=0
        self.clipthreshold=0

        self.fx = ctk.CTkTabview(self.window)
        self.fx.add('Distortion')
        self.fx.add('Delay')
        self.fx.add('Chorus')
        self.fx.add('Phaser')
        self.fx.add('Reverb')
        self.fx.add('Clipping')

        #Chorus
        self.Chorus_Switch = ctk.CTkSwitch(self.fx.tab('Chorus'), text='Off/On', onvalue= 'on', command=self.chorus)
        self.Chorus_Switch.pack()
        self.Chorus_Slider = ctk.CTkSlider(self.fx.tab('Chorus'), from_=0, to=1, command=self.chorusmix)
        self.Chorus_Slider.set(0.5)
        ctk.CTkLabel(self.fx.tab('Chorus'), text='Mix').pack()
        self.Chorus_Slider.pack()
        self.Chorus_mixdisp = ctk.CTkLabel(self.fx.tab('Chorus'), text='50%')
        self.Chorus_mixdisp.pack()

        #Distortion
        self.Disto_Switch = ctk.CTkSwitch(self.fx.tab('Distortion'), onvalue= 'on', text='Off/On', command=self.disto)
        self.Disto_Switch.pack()
        self.Disto_Slider = ctk.CTkSlider(self.fx.tab('Distortion'), from_=10, to=100, command=self.disto_gain)
        self.Disto_Slider.set(25)
        ctk.CTkLabel(self.fx.tab('Distortion'),text='Drive').pack()
        self.Disto_Slider.pack()
        self.Disto_Gaindisp = ctk.CTkLabel(self.fx.tab('Distortion'), text='25 db')
        self.Disto_Gaindisp.pack()

        #Phaser
        self.Phaser_Switch = ctk.CTkSwitch(self.fx.tab('Phaser'), onvalue= 'on', text='Off/On', command=self.phaser)
        self.Phaser_Switch.pack()
        self.Phaser_Slider = ctk.CTkSlider(self.fx.tab('Phaser'), from_=0, to=1, command=self.phasermix)
        self.Phaser_Slider.set(0.5)
        ctk.CTkLabel(self.fx.tab('Phaser'), text='Mix').pack()
        self.Phaser_Slider.pack()
        self.Phaser_mixdisp = ctk.CTkLabel(self.fx.tab('Phaser'), text='50%')
        self.Phaser_mixdisp.pack()

        #Reverb
        self.Rev_Switch = ctk.CTkSwitch(self.fx.tab('Reverb'), onvalue= 'on', text='Off/On', command=self.reverb)
        self.Rev_Switch.pack()
        self.Rev_Slider = ctk.CTkSlider(self.fx.tab('Reverb'), from_=0, to=1, command=self.revsize)
        self.Rev_Slider.set(0.5)
        ctk.CTkLabel(self.fx.tab('Reverb'), text='Room Size').pack()
        self.Rev_Slider.pack()
        self.Rev_sizedisp = ctk.CTkLabel(self.fx.tab('Reverb'), text='50')
        self.Rev_sizedisp.pack()

        #Delay
        self.Del_Switch = ctk.CTkSwitch(self.fx.tab('Delay'), onvalue= 'on', text='Off/On', command=self.delay)
        self.Del_Switch.pack()
        self.Del_Slider = ctk.CTkSlider(self.fx.tab('Delay'), from_=0, to=3, command=self.deltime)
        self.Del_Slider.set(0.5)
        ctk.CTkLabel(self.fx.tab('Delay'), text='Time').pack()
        self.Del_Slider.pack()
        self.Del_timedisp = ctk.CTkLabel(self.fx.tab('Delay'), text='0.5 seconds')
        self.Del_timedisp.pack()

        #Clipping
        self.Clip_Switch = ctk.CTkSwitch(self.fx.tab('Clipping'), onvalue= 'on', text='Off/On', command=self.clip)
        self.Clip_Switch.pack()
        self.Clip_Slider = ctk.CTkSlider(self.fx.tab('Clipping'), from_=-20, to=-1, number_of_steps=19, command=self.clipthresh)
        self.Clip_Slider.set(-6)
        ctk.CTkLabel(self.fx.tab('Clipping'), text='Threshold').pack()
        self.Clip_Slider.pack()
        self.Clip_Thrdisp = ctk.CTkLabel(self.fx.tab('Clipping'), text='-6 db')
        self.Clip_Thrdisp.pack()

        #Bitcrusher
        self.bit_slider = ctk.CTkSlider(self.window, from_=0, to=32, number_of_steps=32, command=self.bitcrush)
        self.bit_display = ctk.CTkLabel(self.window, text='Bit depth')
        self.bit_button = ctk.CTkButton(self.window, text='Use current Bit depth setting', command=self.bitcrush_print)

        #Resample
        self.sample_entry = ctk.CTkEntry(self.window, placeholder_text='Enter sample rate')
        self.sample_button = ctk.CTkButton(self.window, text='Resample', command=self.resample)

        #Pitch Shifter
        self.pitch_slider = ctk.CTkSlider(self.window, from_=-12, to=12, number_of_steps=24, command=self.pitch)
        self.pitch_display = ctk.CTkLabel(self.window, text='Pitch Shift (semi-tones)')
        self.pitch_button = ctk.CTkButton(self.window, text='Use current pitch setting', command=self.pitch_print)

    #Clear Effects Button
        self.clear_button = ctk.CTkButton(self.window,
                                        text='Clear all effects from signal chain',
                                        command=self.clear_chain,
                                        fg_color='transparent',
                                        border_width=4,
                                        font=('Helvetica', 18, 'bold'))
    #Render Button
        self.render_button = ctk.CTkButton(self.window,text="Render", command=self.render,
                                           font= ('Helvetica', 52, 'bold'))

        self.window.mainloop()

#Commands
    #On/off logic for Recording Button
    def click(self):
        if self.switch:
            self.switch = False
            self.r.set('Click Here to Record')
            self.rec_button.configure(fg_color='#333333')
            self.rec_button.configure(hover_color='#2e2e2e')
            self.clock.configure(text='00:00:00')

        else:
            self.switch = True
            self.r.set('Recording... \n Click again to stop')
            self.rec_button.configure(fg_color='red')
            self.rec_button.configure(hover_color='red')
            threading.Thread(target=self.record).start()

    #Recording using pyaudio
    def record(self):
        self.Format = pyaudio.paInt16
        self.Channels = 1
        self.Rate = 41000
        self.Buffer = 1024

        pa = pyaudio.PyAudio()
        stream = pa.open(format=self.Format,
                         channels=self.Channels,
                         rate=self.Rate,
                         input=True,
                         frames_per_buffer=self.Buffer)

        frames = []
        start = time.time()
        while self.switch:
            data = stream.read(self.Buffer)
            frames.append(data)

            passed = time.time() - start
            secs = passed % 60
            mins = passed // 60
            hours = mins // 60

            self.clock.configure(text=f'{int(hours):02d}:{int(mins):02d}:{int(secs):02d}')

        stream.stop_stream()
        stream.close()
        pa.terminate()

    #File naming System / Write to file
        self.num = 0
        self.filename = f"sample{self.num}.wav"
        exists = True
        while exists:
            if os.path.exists(f"sample{self.num}.wav"):
                self.num += 1
            else:
                exists = False

        wavefile = wave.open(f"sample{self.num}.wav", 'wb')
        wavefile.setnchannels(self.Channels)
        wavefile.setsampwidth(pa.get_sample_size(self.Format))
        wavefile.setframerate(self.Rate)
        wavefile.writeframes(b''.join(frames))
        wavefile.close()

    #Opens the rest of the objects
        self.bit_slider.grid(row=0, column=0, sticky='')
        self.bit_display.grid(row=0, column=0, sticky='n', pady=0)
        self.bit_button.grid(row=0, column=0, sticky='s', pady=0)
        ctk.CTkLabel(self.window, text='Set effect parameters BEFORE enabling').grid(row=0, column=3, sticky='n')
        self.fx.grid(row=0, column=3, rowspan=2, sticky='ns', pady=20)
        self.sample_button.grid(row=1, column=0, sticky='s', pady=100)
        self.sample_entry.grid(row=1, column=0, sticky='')

        self.play_button.grid(row=3, column=1, sticky='news')
        self.clear_button.grid(row=3, column=0, sticky='news')

        self.open_button.grid(row=4, column=0, sticky='news')
        self.render_button.grid(row=4, column=1, columnspan=2, sticky='news', pady=0)
        self.pitch_slider.grid(row=4, column=3, sticky='', pady=0)
        self.pitch_display.grid(row=4, column=3, sticky='n', pady=0)
        self.pitch_button.grid(row=4,column=3, sticky='s', pady=0)




    #Opens waveform view of current file with matplotlib (shows current file name)
    def open(self):
        file = wave.open(f"sample{self.num}.wav", 'rb')

        rate2 = file.getframerate()
        frames = file.getnframes()
        signal_wave = file.readframes(-1)

        file.close()

        time = frames / rate2

        ARRAY = np.frombuffer(signal_wave, dtype=np.int16)

        times = np.linspace(0, time, num=frames)

        plt.figure(figsize=(15, 5))
        plt.plot(times, ARRAY)
        plt.ylabel('Signal Wave')
        plt.xlabel('Time (s)')
        plt.xlim(0, time)
        plt.title(f'sample{self.num}.wav')
        plt.show()

    #Play and Stop
    def play(self):
        pygame.mixer.init()
        pygame.mixer.music.load(f"sample{self.num}.wav")
        pygame.mixer.music.play(loops=0)
        self.stop_button.grid(row=3, column=2, sticky='news')
    def restart(self):
        pygame.mixer.music.stop()

    #Pedalboard parameters and effects (appended to self.board as a list)

    def chorusmix(self, mix):
        self.Chorus_mixdisp.configure(text=str(mix*100)[0:2] + '%')
        if mix == 1:
            self.Chorus_mixdisp.configure(text='100%')
        self.chorusamount=mix

    def chorus(self):
        if self.Chorus_Switch.get() == 'on':
            self.board.append(Chorus(mix=self.chorusamount))
            print(self.board)
        else:
            print(self.board)

    def disto_gain(self, drive):
        self.Disto_Gaindisp.configure(text=str(drive)[0:3] + ' db')
        if drive == 100:
            self.Disto_Gaindisp.configure('100 db')
        self.distoamount=drive

    def disto(self):
        if self.Disto_Switch.get() == 'on':
            self.board.append(Distortion(drive_db=self.distoamount))
            print(self.board)

    def phasermix(self, phasermix):
        self.Phaser_mixdisp.configure(text=str(phasermix*100)[0:2] + '%')
        if phasermix == 1:
            self.Phaser_mixdisp.configure(text='100%')
        self.phaseramount = phasermix

    def phaser(self):
        if self.Phaser_Switch.get() == 'on':
            self.board.append(Phaser(mix=self.phaseramount))
            print(self.board)

    def revsize(self, RevSize):
        self.Rev_sizedisp.configure(text=str(RevSize * 100)[0:2])
        if RevSize == 1:
            self.Rev_sizedisp.configure(text='100')
        self.roomsize = RevSize
    def reverb(self):
        if self.Rev_Switch.get() == 'on':
            self.board.append(Reverb(room_size=self.roomsize, wet_level=.6))
            print(self.board)
        else:
            print(self.board)

    def deltime(self, time):
        self.Del_timedisp.configure(text=str(round(time, 2))+ ' seconds')
        self.delaytime = round(time, 2)


    def delay(self):
        if self.Del_Switch.get() == 'on':
            self.board.append(Delay(delay_seconds=self.delaytime))
            print(self.board)

    def clipthresh(self, thresh):
        self.Clip_Thrdisp.configure(text=str(thresh)[0:3]+' db')
        self.clipthreshold = thresh
    def clip(self):
        if self.Clip_Switch.get() == 'on':
            self.board.append(Clipping(threshold_db=self.clipthreshold))
            print(self.board)

    def pitch(self, x):
        self.pitch_amount = x
        self.pitch_display.configure(text=str(x).rstrip('.0')+' semi-tones')

    def pitch_print(self):
        self.board.append(PitchShift(float(self.pitch_amount)))
        print(self.board)
    def bitcrush(self, x):
        self.bit_depth = x
        self.bit_display.configure(text=str(x).rstrip(".0")+' bits')

    def bitcrush_print(self):
        self.board.append(Bitcrush(float(self.bit_depth)))
        print(self.board)
    def resample(self):
        self.board.append(Resample(target_sample_rate=int(self.sample_entry.get())))
        print(self.board)

    #Renders effects to new file using Pedalboard then clears pedalboard list and resets effect switches
    #self.board is put into a Pedalboard() command
    def render(self):
        with AudioFile(f"sample{self.num}.wav").resampled_to(self.Rate) as f:
            self.audio = f.read(f.frames)

        self.BOARD = Pedalboard(self.board)

        self.effected = self.BOARD(self.audio, self.Rate)
        self.num += 1
        with AudioFile(f"sample{self.num}.wav", 'w', self.Rate, self.effected.shape[0]) as f:
            f.write(self.effected)

        self.board.clear()
        self.Chorus_Switch.deselect()
        self.Disto_Switch.deselect()
        self.Phaser_Switch.deselect()
        self.Rev_Switch.deselect()
        self.Del_Switch.deselect()
        self.Clip_Switch.deselect()

    #Clear pedalboard list
    def clear_chain(self):

            self.board.clear()


Ample_Sample()