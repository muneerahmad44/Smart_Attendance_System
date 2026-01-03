from vector_dbs.store_faculty import add_faculty_member,retrieve_from_db,delete_faculty_member
from src.calculate_embeddings import generate

from src.attendance_logic import in_attendance,mark_absent_camera
import time

class SmartAttendanceSystem:
    def __init__(self):
        pass
    def add_member(self,create_db:bool,add_faculty:bool,img=None,faculty_id=None, faculty_metadata=None):


        if add_faculty==True:
           faculty_embedding=generate(img)
           add_faculty_member(faculty_id,faculty_embedding,faculty_metadata)


    def delete_member(self,id:str):
        result=delete_faculty_member(id)
        

    def retrive(self,img):
        faculty_embedding=generate(img)
        results=retrieve_from_db(faculty_embedding)
        return results
    
    def in_mark_attendance(self,img):
        s_time=time.time()
        result=in_attendance(img)
        e_time=time.time()
        # print(f"total time in mark attendance function: {e_time-s_time}")
        return result
    
    def out_mark_absent(self,img):
        result=mark_absent_camera(img)
        return result
    
    

# img=cv2.imread("/home/muneer/Data/computer vision learning/projects/smart attendance system/both.jpeg")
# img_r=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

# # attendance.add_member(False,True,img_r,"1",{"name":"huzaifa","role":"Lecturer","deptt":"Computer Engineering"})
# # attendance.delete_member("3")
# # # s_time=time.time()
# # img_to_send=cv2.imread("/home/muneer/Data/computer vision learning/projects/smart attendance system/mumtaz.jpeg")
# # img_rgb=cv2.cvtColor(img_to_send,cv2.COLOR_BGR2RGB)

# # # # result=attendance.mark_attendance(img_rgb)
# # # # print(result)
# attendance=SmartAttendanceSystem()     
# # attendance.add_member(False,True,img_r,"3",{'name':'zain',"role":"lecturer","deptt":"CS"})
# # # attendance.delete_member('1')
# result=attendance.retrive(img_r)
# print(result)

# # print(f"total time taken to process one image is {e_time-s_time}")