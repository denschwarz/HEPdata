from entry import entry
from imageHelpers import convertToPNG

class submission:
    def __init__(self, abstract):
        self.__abstract = abstract
        self.__entries = []

    def addEntry(self, image, title, caption, obs, keywords, location):
        if image is not None:
            # convertToPNG(image)
            imagename = image.replace(".pdf", ".png")
            thumbname = "thumb_"+imagename
        else:
            imagename = None
            thumbname = None
        self.__entries.append(entry(imagename, thumbname, title, caption, obs, keywords, location))


    def makeFile(self):
        with open("output/submission.yaml", "w") as f:
            f.write('---\n')
            f.write('comment: ')
            abstractFile = open(self.__abstract, 'r')
            for line in abstractFile.readlines():
                f.write("  "+line)
            f.write("data_license:\n")
            f.write("  description: The content can be shared and adapted but you must             give\n")
            f.write("    appropriate credit and cannot restrict access to others.\n")
            f.write("  name: cc-by-4.0\n")
            f.write("  url: https://creativecommons.org/licenses/by/4.0/\n")
            for entry in self.__entries:
                f.write("---\n")
                if entry.image is not None:
                    f.write("additional_resources:\n")
                    f.write("- description: Image file\n")
                    f.write("  location: "+entry.image+"\n")
                    f.write("- description: Thumbnail image file\n")
                    f.write("  location: "+entry.thumb+"\n")
                f.write("data_file: "+entry.title+".yaml\n")
                f.write("description: "+entry.caption+"\n")
                f.write("keywords:\n")
                f.write("- name: reactions\n")
                f.write("  values:\n")
                f.write("  - P P --> t t\n")
                f.write("- name: observables\n")
                f.write("  values:\n")
                f.write("  - "+entry.obs+"\n")
                f.write("- name: cmenergies\n")
                f.write("  values:\n")
                f.write("  - 13000\n")
                f.write("- name: phrases\n")
                f.write("  values:\n")
                for k in entry.keywords:
                    f.write("  - "+k+"\n")
                f.write("location: "+entry.location+"\n")
                f.write("name: "+entry.title+"\n")
