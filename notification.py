import sys

if(sys.platform == "darwin"):
    import Foundation
    import objc

    NSUserNotification = objc.lookUpClass('NSUserNotification')
    NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')

    def notify(title="", subtitle="", info_text="", delay=0, sound=False, userInfo={}):
        notification = NSUserNotification.alloc().init()
        notification.setTitle_(title)
        notification.setSubtitle_(subtitle)
        notification.setInformativeText_(info_text)
        notification.setUserInfo_(userInfo)
        if sound:
            notification.setSoundName_("NSUserNotificationDefaultSoundName")
        notification.setDeliveryDate_(Foundation.NSDate.dateWithTimeInterval_sinceDate_(delay, Foundation.NSDate.date()))
        NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)
elif(sys.platform == "win32"):
    from plyer import notification

    def notify(title="", subtitle=""):
        notification.notify(title=title, message=subtitle, timeout=0)