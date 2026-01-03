from store_faculty import add_faculty_member,delete_faculty_member
from src.calculate_embeddings import generate
import cv2
path="/home/muneer/Data/computer vision learning/projects/smartattendancesystem2/vector_dbs/muneer.jpg"
img=cv2.imread(path)
# img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
embedings=generate(img)
faculty_id="4"
faculty_embeding=embedings[0] # single embedding as list of floats

faculty_metadata={"name":"Muneer khan","deptt":"Computer Science","role":"lecturer"}
# delete_faculty_member("3")
status=add_faculty_member(faculty_id,faculty_embeding,faculty_metadata)
