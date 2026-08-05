import os
import subprocess
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.core.window import Window

# تعيين خلفية التطبيق
Window.clearcolor = (0.1, 0.1, 0.15, 1)

class VideoToAudioApp(App):
    def build(self):
        self.title = '🎬 فيديو ➜ صوت'
        
        # التصميم الرئيسي
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # عنوان
        title_label = Label(
            text='🎬 تحويل فيديو إلى صوت',
            font_size=30,
            color=(0.2, 0.8, 0.2, 1),
            size_hint=(1, 0.15)
        )
        layout.add_widget(title_label)
        
        # زر اختيار الفيديو
        self.select_btn = Button(
            text='📂 اختيار فيديو',
            font_size=20,
            background_color=(0.2, 0.5, 0.8, 1),
            size_hint=(1, 0.15)
        )
        self.select_btn.bind(on_press=self.select_video)
        layout.add_widget(self.select_btn)
        
        # عرض اسم الملف
        self.file_label = Label(
            text='لم يتم اختيار ملف',
            font_size=16,
            color=(0.8, 0.8, 0.8, 1),
            size_hint=(1, 0.1)
        )
        layout.add_widget(self.file_label)
        
        # زر التحويل
        self.convert_btn = Button(
            text='🔄 تحويل إلى صوت',
            font_size=20,
            background_color=(0.2, 0.7, 0.2, 1),
            size_hint=(1, 0.15),
            disabled=True
        )
        self.convert_btn.bind(on_press=self.convert_video)
        layout.add_widget(self.convert_btn)
        
        # شريط التقدم
        self.progress = ProgressBar(
            max=100,
            value=0,
            size_hint=(1, 0.1)
        )
        layout.add_widget(self.progress)
        
        # حالة التطبيق
        self.status_label = Label(
            text='✅ جاهز للعمل',
            font_size=16,
            color=(0.5, 0.8, 0.5, 1),
            size_hint=(1, 0.1)
        )
        layout.add_widget(self.status_label)
        
        self.video_path = None
        self.output_path = None
        
        return layout
    
    def select_video(self, instance):
        """فتح مستكشف الملفات لاختيار فيديو"""
        content = BoxLayout(orientation='vertical', spacing=10)
        
        filechooser = FileChooserIconView(
            path='/storage/emulated/0/',
            filters=['*.mp4', '*.avi', '*.mkv', '*.mov', '*.3gp'],
            size_hint=(1, 0.9)
        )
        content.add_widget(filechooser)
        
        select_btn = Button(
            text='✅ اختيار',
            size_hint=(1, 0.1),
            background_color=(0.2, 0.7, 0.2, 1)
        )
        content.add_widget(select_btn)
        
        popup = Popup(
            title='📂 اختر ملف فيديو',
            content=content,
            size_hint=(0.9, 0.9)
        )
        
        def on_select(btn):
            if filechooser.selection:
                self.video_path = filechooser.selection[0]
                self.file_label.text = f'📄 {os.path.basename(self.video_path)}'
                self.convert_btn.disabled = False
                self.status_label.text = '✅ تم اختيار الفيديو'
                self.status_label.color = (0.2, 0.8, 0.2, 1)
                popup.dismiss()
            else:
                self.status_label.text = '⚠️ لم يتم اختيار ملف'
                self.status_label.color = (0.9, 0.7, 0.1, 1)
        
        select_btn.bind(on_press=on_select)
        popup.open()
    
    def convert_video(self, instance):
        """تحويل الفيديو إلى صوت"""
        if not self.video_path:
            return
        
        # تعطيل الأزرار
        self.select_btn.disabled = True
        self.convert_btn.disabled = True
        self.status_label.text = '⏳ جاري التحويل...'
        self.status_label.color = (0.3, 0.6, 0.9, 1)
        self.progress.value = 0
        
        # تشغيل التحويل في خيط منفصل
        threading.Thread(target=self._convert, daemon=True).start()
    
    def _convert(self):
        """دالة التحويل (تعمل في الخلفية)"""
        try:
            # تحديد مسار الإخراج
            base_name = os.path.splitext(self.video_path)[0]
            self.output_path = f"{base_name}_audio.mp3"
            
            # أمر FFmpeg
            cmd = [
                "ffmpeg", "-i", self.video_path,
                "-vn", "-acodec", "libmp3lame",
                "-ac", "2", "-b:a", "192k",
                "-y", self.output_path
            ]
            
            # تنفيذ الأمر
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # تحديث التقدم
            while True:
                output = process.stderr.readline()
                if output == '' and process.poll() is not None:
                    break
                if 'time=' in output:
                    try:
                        time_str = output.split('time=')[1].split(' ')[0]
                        parts = time_str.split(':')
                        total_seconds = int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
                        # تحديث واجهة المستخدم
                        Clock.schedule_once(lambda dt, s=total_seconds: self.update_progress(s), 0)
                    except:
                        pass
            
            # التحقق من النجاح
            if os.path.exists(self.output_path) and os.path.getsize(self.output_path) > 0:
                Clock.schedule_once(lambda dt: self.conversion_success(), 0)
            else:
                Clock.schedule_once(lambda dt: self.conversion_failed("فشل إنشاء الملف"), 0)
                
        except Exception as e:
            Clock.schedule_once(lambda dt: self.conversion_failed(str(e)), 0)
    
    def update_progress(self, seconds):
        """تحديث شريط التقدم"""
        # تقدير التقدم (بسيط)
        progress = min(100, int(seconds * 2))
        self.progress.value = progress
    
    def conversion_success(self):
        """عند نجاح التحويل"""
        self.select_btn.disabled = False
        self.convert_btn.disabled = False
        self.progress.value = 100
        self.status_label.text = f'✅ تم التحويل! الملف: {os.path.basename(self.output_path)}'
        self.status_label.color = (0.2, 0.8, 0.2, 1)
        
        # عرض رسالة نجاح
        popup = Popup(
            title='✅ نجاح!',
            content=Label(text=f'تم تحويل الفيديو إلى صوت بنجاح!\n\n📁 {os.path.basename(self.output_path)}'),
            size_hint=(0.8, 0.4)
        )
        popup.open()
    
    def conversion_failed(self, error):
        """عند فشل التحويل"""
        self.select_btn.disabled = False
        self.convert_btn.disabled = False
        self.progress.value = 0
        self.status_label.text = f'❌ فشل: {error[:50]}...'
        self.status_label.color = (0.9, 0.2, 0.2, 1)

if __name__ == '__main__':
    VideoToAudioApp().run()
