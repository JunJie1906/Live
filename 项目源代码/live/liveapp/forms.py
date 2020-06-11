from django import forms


class getRoomForm(forms.Form):
    roomID = forms.CharField(label="请输入你要进入房间ID：", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))

class launchForm(forms.Form):
    LiveName = forms.CharField(label="请输入将要开启的直播间的名字：",max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))


