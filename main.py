# /// script
# requires-python = ">=3.12"
# dependencies = [
#   'requests',
#   'beautifulsoup4',
# ]
# ///

# Test your linker here

from src.dandanzan import DandanzanLinker

if __name__ == "__main__":
    print(DandanzanLinker().detail("dianying-20106447"))
