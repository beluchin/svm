
def report_nothing_to_undo():
    print('nothing to undo')
    
def report_missing_videos(vs):
    print("some videos don't exist\n%s" % '\n'.join(vs))

def report_video_failed_to_rename(v):
    if not report_video_failed_to_rename.called:
        report_video_failed_to_rename.called = True
        print("some videos failed to rename")
    print(v)
report_video_failed_to_rename.called = False