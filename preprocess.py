import argparse
import text
from utils import load_filepaths_and_text
from tqdm import tqdm

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--type", default="ljs", help="ljs, vctk")
  parser.add_argument("--out_extension", default="cleaned")
  parser.add_argument("--filelists", nargs="+", default=["filelists/ljs_audio_text_val_filelist.txt", "filelists/ljs_audio_text_train_filelist.txt"])
  parser.add_argument("--text_cleaners", nargs="+", default=["korean_cleaners"])
  parser.add_argument("--add_dir", default="filelists/wavs/")
  parser.add_argument("--add_extension", default="")

  args = parser.parse_args()
  if args.type=="vctk":
    text_pos = 2
  else:
    text_pos = 1
  for filelist in args.filelists:
    print("START:", filelist)
    filepaths_and_text = load_filepaths_and_text(filelist)
    for i in tqdm(range(len(filepaths_and_text))):
      original_text = filepaths_and_text[i][text_pos]
      cleaned_text = text._clean_text(original_text, args.text_cleaners)
      filepaths_and_text[i][text_pos] = cleaned_text
      filepaths_and_text[i][0]=args.add_dir+filepaths_and_text[i][0]+args.add_extension

    new_filelist = filelist + "." + args.out_extension
    with open(new_filelist, "w", encoding="utf-8") as f:
      if args.type=="ljs":
        f.writelines(["|".join(x[:2]) + "\n" for x in filepaths_and_text])
      else:
        f.writelines(["|".join(x) + "\n" for x in filepaths_and_text])