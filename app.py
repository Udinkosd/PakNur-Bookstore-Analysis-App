import streamlit as st
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
import matplotlib.ticker as mtick
import streamlit_lottie as st_lottie
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import linkage
import plotly.figure_factory as ff

import urllib.request
import seaborn as sns
import numpy as np
import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from pandas import json_normalize

from streamlit_lottie import st_lottie

st.set_page_config(page_title="PakNur Bookstore Analysis App", layout="wide", page_icon="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxZW0iIGhlaWdodD0iMWVtIiB2aWV3Qm94PSIwIDAgMTI4IDEyOCI+PHBhdGggZmlsbD0iI2M2MjgyOCIgZD0ibTcwLjI0IDEwMC43OWw0OC41NSA0LjYyYzQuNTcuNDQgNS43NC0yLjExIDUuNzQtNC4yN2wtLjA1LTIuNjJsLTU5LjcxLTguNDJjMCAyLjk5IDIuNDMgMTAuNjkgNS40NyAxMC42OSIvPjxwYXRoIGZpbGw9IiNmNDQzMzYiIGQ9Im03Mi4wMSA5OC41MWw3LjY0LjY3bDQwLjkxIDMuOTVjMi4yIDAgMy45Ny0xLjc1IDMuOTctMy45MWwtMi4xNy02Ni4yNmMwLTIuMTYtMS43OC0zLjkxLTMuOTctMy45MWwtNDYuMzgtNC4zOGMtMy4wNCAwLTUuNTEgMi40My01LjUxIDUuNDJ2NjNjMCAyLjk5IDIuNDYgNS40MiA1LjUxIDUuNDIiLz48cGF0aCBmaWxsPSIjYzYyODI4IiBkPSJtNTcuNzYgMTAwLjc5bC00OC41NSA0LjYyYy00LjU3LjQ0LTUuNzQtMi4xMS01Ljc0LTQuMjdsLjA1LTIuNjJsNTkuNzEtOC40M2MwIDMtMi40MyAxMC43LTUuNDcgMTAuNyIvPjxwYXRoIGZpbGw9IiNmNDQzMzYiIGQ9Im01NS45OSA5OC41MWwtNy41OC42N2wtNDAuOTcgMy45NmMtMi4yIDAtMy45Ny0xLjc1LTMuOTctMy45MWwyLjE3LTY2LjI2YzAtMi4xNiAxLjc4LTMuOTEgMy45Ny0zLjkxbDQ2LjM4LTQuMzhjMy4wNCAwIDUuNTEgMi40MyA1LjUxIDUuNDJ2NjNjMCAyLjk4LTIuNDYgNS40MS01LjUxIDUuNDEiLz48cGF0aCBmaWxsPSIjNDI0MjQyIiBkPSJNNzguNzUgODMuNjhINDkuMjdsLS45IDE1LjUzbDkuMi44NnMxLjk3IDQuOTIgNi40MyA0LjkyczYuNDMtNC45MiA2LjQzLTQuOTJsOS4yLS44NnoiLz48cGF0aCBmaWxsPSJub25lIiBzdHJva2U9IiM2MTYxNjEiIHN0cm9rZS1taXRlcmxpbWl0PSIxMCIgc3Ryb2tlLXdpZHRoPSIyLjUiIGQ9Im03OS41NCAxMDAuNDNsLTguNTctLjc0bS0yMi41MS43NGw4LjU3LS43NCIvPjxwYXRoIGZpbGw9IiM5NGM2ZDYiIGQ9Im0xMTkuNjUgMzIuODJsLTQtNS41TDY0IDg2LjAybC01MS42NS01OC43bC00IDUuNWwtLjU2IDY1LjM1czEwLjYyIDEuMzMgMjQuODEtLjExYzEyLjM2LTEuMjUgMTguMTgtNC40NSAyMi4zMS0zLjYyYzQuOTYgMSA1Ljg2IDQuMDUgNi4wMiA0LjU3Yy40NSAxLjQ0IDEuMzQgMi41NiAzLjA3IDIuNTZzMi41LS42IDMuMDMtMi4zOGMuMTYtLjUyIDEuMS0zLjc0IDYuMDYtNC43NGM0LjEzLS44MyA5Ljk1IDIuMzcgMjIuMzEgMy42MmMxNC4xOSAxLjQ0IDI0LjgxLjExIDI0LjgxLjExeiIvPjxsaW5lYXJHcmFkaWVudCBpZD0ibm90b09wZW5Cb29rMCIgeDE9IjUwLjg4NSIgeDI9IjUwLjYzOCIgeTE9Ijg4LjIwMSIgeTI9IjcwLjg5OCIgZ3JhZGllbnRUcmFuc2Zvcm09Im1hdHJpeCgtMSAwIDAgMSAxNjguMTI4IDApIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHN0b3Agb2Zmc2V0PSIuMjY3IiBzdG9wLWNvbG9yPSIjODJhZWMwIi8+PHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjODJhZWMwIiBzdG9wLW9wYWNpdHk9IjAiLz48L2xpbmVhckdyYWRpZW50PjxwYXRoIGZpbGw9InVybCgjbm90b09wZW5Cb29rMCkiIGQ9Im0xMTQuMyA5MS44N2wuMTYtMjYuMzloNS40N2wuMjggMzIuNjlzLTQuMzUtMS42OS01LjkxLTYuMyIvPjxsaW5lYXJHcmFkaWVudCBpZD0ibm90b09wZW5Cb29rMSIgeDE9Ijk4LjIxMSIgeDI9IjU1LjQiIHkxPSI4NC42MDEiIHkyPSI4NC42MDEiIGdyYWRpZW50VHJhbnNmb3JtPSJtYXRyaXgoLTEgMCAwIDEgMTY4LjEyOCAwKSIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPjxzdG9wIG9mZnNldD0iMCIgc3RvcC1jb2xvcj0iIzJmNzg4OSIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzgyYWVjMCIvPjwvbGluZWFyR3JhZGllbnQ+PHBhdGggZmlsbD0idXJsKCNub3RvT3BlbkJvb2sxKSIgZD0ibTExNC41NSA3Ni40OWwtLjI1IDE1LjM5cy0xMS45Ni0uNjItMzEuMDEtMy45MkM3MC44MyA4NS44IDY0IDkyLjcyIDY0IDkyLjcybC0uMTEtMTYuMjN6Ii8+PGxpbmVhckdyYWRpZW50IGlkPSJub3RvT3BlbkJvb2syIiB4MT0iNTcuOTc5IiB4Mj0iMTUuMjYzIiB5MT0iODQuNjAxIiB5Mj0iODQuNjAxIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjMmY3ODg5Ii8+PHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjODJhZWMwIi8+PC9saW5lYXJHcmFkaWVudD48cGF0aCBmaWxsPSJ1cmwoI25vdG9PcGVuQm9vazIpIiBkPSJtMTMuNDUgNzYuNDlsLjI1IDE1LjM5czExLjk2LS42MiAzMS4wMS0zLjkyQzU3LjE3IDg1LjggNjQgOTIuNzIgNjQgOTIuNzJsLS4xMS0xNi4yM3oiLz48bGluZWFyR3JhZGllbnQgaWQ9Im5vdG9PcGVuQm9vazMiIHgxPSIxMC43NTMiIHgyPSIxMC41MDUiIHkxPSI4OC4yMDEiIHkyPSI3MC44OTgiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj48c3RvcCBvZmZzZXQ9Ii4yNjciIHN0b3AtY29sb3I9IiM4MmFlYzAiLz48c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiM4MmFlYzAiIHN0b3Atb3BhY2l0eT0iMCIvPjwvbGluZWFyR3JhZGllbnQ+PHBhdGggZmlsbD0idXJsKCNub3RvT3BlbkJvb2szKSIgZD0ibTEzLjcgOTEuODdsLS4xNi0yNi4zOUg4LjA2bC0uMjcgMzIuNjlzNC4zNC0xLjY5IDUuOTEtNi4zIi8+PHBhdGggZmlsbD0iI2Y1ZjVmNSIgZD0iTTExNS42NSAyNy4zMnMtMjYuNTQtNC45OS0zOC4xOS01LjY0Yy0xMC45Ni0uNjEtMTMuMjEgNC45Ny0xMy40MyA1LjY0aC0uMDRjLS4yMy0uNjctMi40OC02LjI0LTEzLjQ0LTUuNjRjLTExLjY1LjY1LTM4LjE5IDUuNjQtMzguMTkgNS42NGwtMS4xOCA2NC40czMxLjYtNi42MiAzOS4yNS01Ljc2UzY0IDkyLjcyIDY0IDkyLjcydi0uMDF2LjAxczUuOTMtNS45IDEzLjU4LTYuNzZjNy42NS0uODYgMzkuMjUgNS43NiAzOS4yNSA1Ljc2eiIvPjxwYXRoIGZpbGw9IiM5NGM2ZDYiIGQ9Im01My42MiAyMS42OWwtNS40IDY0LjJjLjg1LS4wMiAxLjYgMCAyLjIuMDdjNy42NC44NSAxMy41OCA2Ljc2IDEzLjU4IDYuNzZsLS4xNy02NS40cy0xLjMtNS4xMi0xMC4yMS01LjYzIiBvcGFjaXR5PSIwLjI2Ii8+PHBhdGggZmlsbD0iIzc1NzU3NSIgZD0iTTI1LjMxIDMwLjE4Yy0yLjcuNDctNC45MS44Ny02LjE3IDEuMDljMCAuNjIgMCAxLjMtLjAxIDIuMDNjMS4xMS0uMiAzLjM3LS42MSA2LjE4LTEuMXptMjQuMzQtMy4yMnYxLjk5YzUuMzMtLjAxIDguMjggMS4zMyA5LjI1IDEuODdjMC0uODMuMDEtMS41Ny4wMS0yLjIyYy0xLjY1LS43NC00LjY3LTEuNjUtOS4yNi0xLjY0bS00LjM0LjI1Yy00LjMzLjQ0LTEwLjM2IDEuMzYtMTUuNjYgMi4yNHYyLjAzYzUuMjYtLjg3IDExLjMtMS44IDE1LjY2LTIuMjZ6bS0xMC42NSA4LjYzYy02LjQ2IDEtMTIuOTQgMi4xNi0xNS41NCAyLjYzdjIuMDNjMi4yNi0uNDEgOC44OS0xLjYxIDE1LjU0LTIuNjR6bTEyLjAzLTEuNTZjLTIuMTEuMTctNC44LjUxLTcuNjkuOTF2Mi4wMmMyLjk1LS40MiA1LjcxLS43NiA3Ljg1LS45NGM3LjE4LS41OSAxMC45NyAxLjE3IDEyLjAzIDEuNzd2LTIuMjNjLTEuOTYtLjg3LTUuODktMi4wNS0xMi4xOS0xLjUzTTI2LjM4IDQ0LjM5Yy0zLjE2LjU0LTUuOCAxLjAxLTcuMjYgMS4yOHYyLjAzYzEuMzEtLjI0IDMuOTktLjcyIDcuMjYtMS4yOHptMzIuNS0xLjM1Yy0xLjk1LS44OC01Ljg5LTIuMDgtMTIuMjUtMS41NWMtNC4wNy4zMy0xMC4zIDEuMjYtMTUuOTEgMi4xOHYyLjAzYzUuNjYtLjkzIDExLjk4LTEuODcgMTYuMDgtMi4yMWM3LjMtLjYgMTEuMSAxLjIzIDEyLjA4IDEuOHptLjAxIDcuMjNjLTEuOTMtLjg4LTUuODktMi4xMS0xMi4zLTEuNThjLS42NS4wNS0xLjM1LjEyLTIuMDkuMnYyLjAxYy44MS0uMDkgMS41Ni0uMTYgMi4yNi0uMjJjNy40NC0uNjEgMTEuMjQgMS4zIDEyLjE0IDEuODRjLS4wMS0uNzUtLjAxLTEuNS0uMDEtMi4yNW0tMTguNzQtLjg0Yy03LjgyIDEuMDctMTcuNTYgMi44LTIxLjAyIDMuNDN2Mi4wM2MzLjA1LS41NiAxMy4wMi0yLjM1IDIxLjAyLTMuNDV6bS0xMS45IDkuMDRjLTMuOTMuNjYtNy4zMyAxLjI3LTkuMTIgMS41OXYyLjAzYzEuNjItLjMgNS4wNy0uOTIgOS4xMi0xLjZ6bTMwLjY1LS45NmMtMS45MS0uODgtNS44OS0yLjE0LTEyLjM2LTEuNjFjLTMuNi4zLTguODggMS4wNS0xMy45NCAxLjg2djIuMDJjNS4xMS0uODIgMTAuNDgtMS41OSAxNC4xLTEuODljNy42My0uNjMgMTEuNDQgMS40MSAxMi4yIDEuODd6bS4wMiAxNC40N2MtMS44Mi0uODctNS43Ni0yLjE4LTEyLjI2LTEuNjl2Mi4wMWM4LjI5LS42NyAxMi4wNSAxLjgxIDEyLjI2IDEuOTZ6bS0zMi41NCAxLjJjLTMuMDguNTMtNS43Ljk5LTcuMjMgMS4yN3YyLjAzYzEuNDEtLjI2IDQuMDUtLjczIDcuMjMtMS4yOHptNC4zNC0uNzJ2Mi4wM2MzLjg4LS42MyA4LjA1LTEuMjcgMTEuNi0xLjcydi0yLjAyYy0zLjUzLjQ0LTcuNyAxLjA3LTExLjYgMS43MW02Ljk1IDYuMTJjLTcuMTYgMS4wNC0xNS4yMSAyLjQ3LTE4LjUxIDMuMDd2Mi4wM2MyLjk5LS41NSAxMS4xOS0yLjAxIDE4LjUxLTMuMDh6bTIxLjI2LjY0Yy0xLjgxLS44OC01Ljg0LTIuMjUtMTIuNTYtMS43Yy0xLjI3LjEtMi43NS4yNy00LjM2LjQ3VjgwYzEuNjctLjIxIDMuMjEtLjM4IDQuNTItLjQ5YzguNTYtLjcxIDEyLjMyIDEuOTUgMTIuMzYgMS45N2wuMDUtLjA2YzAtLjY5IDAtMS40Mi0uMDEtMi4yTTM2LjE4IDY0LjRjLTYuODIgMS4wMi0xNC4wNSAyLjMxLTE3LjA0IDIuODZ2Mi4wM2MyLjY4LS40OSAxMC4wNS0xLjgxIDE3LjA0LTIuODd6bTIyLjczLjM0Yy0xLjg4LS44OC01Ljg3LTIuMTgtMTIuNDMtMS42NGMtMS42OC4xNC0zLjczLjM4LTUuOTUuNjh2Mi4wMmMyLjI5LS4zMSA0LjQtLjU2IDYuMTItLjdjNy44OC0uNjUgMTEuNjkgMS41NCAxMi4yNyAxLjkxYy0uMDEtLjc0LS4wMS0xLjUtLjAxLTIuMjdtMjkuNS0zNS4wM2M4LjI4IDEuMSAxOS4xIDMuMDYgMjIuMDQgMy41OWMwLS43NCAwLTEuNDEtLjAxLTIuMDNjLTMuNDQtLjYzLTEzLjk3LTIuNTEtMjIuMDQtMy41OHYyLjAyem0tNC4zNS0yLjUyYy0uNDMtLjA0LS44NC0uMDgtMS4yMy0uMTFjLTYuMjctLjUyLTEwLjE5LjY1LTEyLjE2IDEuNTJjMCAuNjUuMDEgMS40LjAxIDIuMjJjMS4xMi0uNjIgNC45MS0yLjMzIDExLjk5LTEuNzVjLjQ0LjA0LjkxLjA4IDEuMzkuMTN6bTE4LjMgMTEuODlhNjczIDY3MyAwIDAgMSA4LjEgMS40M3YtMi4wM2MtMS41Ny0uMjktNC41NS0uODItOC4xLTEuNDJ6bS00LjM0LTIuNzVjLTUuNDEtLjg3LTExLjI1LTEuNzMtMTUuMTMtMi4wNWMtNi4zLS41Mi0xMC4yMy42Ni0xMi4yIDEuNTN2Mi4yM2MxLjA2LS42IDQuODUtMi4zNiAxMi4wMy0xLjc3YzMuOTEuMzIgOS44NCAxLjIgMTUuMjkgMi4wOHYtMi4wMnptLS44NCA3LjA2djIuMDJjNS44MS45MyAxMS4yMiAxLjkxIDEzLjI4IDIuMjl2LTIuMDNjLTIuMzMtLjQyLTcuNjQtMS4zNy0xMy4yOC0yLjI4TTg4LjQgNDkuM2MtMi4wMS0uMjYtMy44Ny0uNDgtNS40MS0uNmMtNi40MS0uNTMtMTAuMzcuNy0xMi4zIDEuNTh2Mi4yNWMuOS0uNTMgNC43MS0yLjQ1IDEyLjE0LTEuODRjMS41OC4xMyAzLjUuMzUgNS41Ny42M3ptNC4zNS42MXYyLjAyYzcuMjUgMS4wOCAxNS4wNiAyLjQ5IDE3LjcgMi45N3YtMi4wM2MtMi45OC0uNTUtMTAuNjMtMS45MS0xNy43LTIuOTZtLjg4IDcuMzNjLTMuOTUtLjYtNy43OC0xLjExLTEwLjU4LTEuMzRjLTYuNDgtLjUzLTEwLjQ2LjczLTEyLjM2IDEuNjF2Mi4yNmMuNzYtLjQ3IDQuNTctMi41IDEyLjItMS44N2MyLjgzLjIzIDYuNzQuNzYgMTAuNzUgMS4zN3YtMi4wM3ptNC4zNC42OHYyLjAzYzUuNDQuODggMTAuNDIgMS43OCAxMi40NyAyLjE1di0yLjAzYy0yLjI4LS40Mi03LjE4LTEuMy0xMi40Ny0yLjE1bTcuMDcgOC4zOHYyLjAzYzIuMzYuNDEgNC4yOS43NiA1LjM5Ljk2di0yLjAzYy0xLjItLjIyLTMuMS0uNTYtNS4zOS0uOTZtLTE1Ljc1IDQuNzFjLTIuMjktLjMxLTQuNDEtLjU2LTYuMTMtLjdjLTYuNjQtLjU1LTEwLjY1Ljc5LTEyLjQ5IDEuNjd2Mi4yOGMuMjEtLjE1IDMuOTktMi42NSAxMi4zNC0xLjk2YzEuNzYuMTQgMy45NC40IDYuMy43MnYtMi4wMXptNC4zNC42MnYyLjAyYzYuODggMS4wNCAxNC4xIDIuMzQgMTYuOCAyLjgzdi0yLjAzYy0zLS41NC0xMC4wOC0xLjgtMTYuOC0yLjgybTMuNTUgNy43NWMtNS4wNy0uODEtMTAuMzctMS41Ny0xMy45Ny0xLjg3Yy02LjczLS41NS0xMC43NS44My0xMi41NiAxLjd2Mi4ybC4wNS4wNmMuMDMtLjAyIDMuNzktMi42OCAxMi4zNi0xLjk3YzMuNjMuMyA5LjAyIDEuMDggMTQuMTQgMS45di0yLjAyem00LjM1LjcydjIuMDNjMy44OS42NSA3LjIxIDEuMjUgOC44OSAxLjU2di0yLjAzYy0xLjgzLS4zNC01LjExLS45My04Ljg5LTEuNTZtLTE4LjYtMTcuMDFjLTYuNDYtLjUxLTEwLjQuNzgtMTIuMjYgMS42NXYyLjI3Yy41OC0uMzcgNC4zOC0yLjU2IDEyLjI2LTEuOTF6bTQuMzUuNDZ2Mi4wMWM0LjEyLjUyIDkuMDcgMS4zIDEzLjQyIDIuMDJ2LTIuMDNjLTQuMzgtLjcyLTkuMzMtMS40OS0xMy40Mi0ybS03LjU2LTIyLjE4Yy00LjQ4LjAzLTcuNDMuOTUtOS4wMiAxLjY3djIuMjRjLjg0LS40OCAzLjcxLTEuODcgOS4wMi0xLjkyem00LjM0LjIydjIuMDFjMi40OS4yNSA1LjU4LjY3IDguNzcgMS4xNHYtMi4wMmMtMy4yLS40OC02LjI4LS44OS04Ljc3LTEuMTMiIG9wYWNpdHk9IjAuNSIvPjxwYXRoIGZpbGw9IiM2MTYxNjEiIGQ9Ik03MS4xNiA5OC40NWMtMS4xMi0uMS0yLjE1LjU5LTIuNTEgMS42NmMtLjU0IDEuNjMtMS44IDMuNzYtNC42NSAzLjc2Yy0yLjg4IDAtNC4xNS0yLjE0LTQuNy0zLjc3YTIuNDE1IDIuNDE1IDAgMCAwLTIuNDgtMS42NGwtLjM5LjAzbC4wMS4zMmE3LjU1IDcuNTUgMCAwIDAgNy41NSA3LjU1YTcuNTUgNy41NSAwIDAgMCA3LjU1LTcuNTVjMC0uMS0uMDEtLjMzLS4wMS0uMzN6Ii8+PC9zdmc+")


df = pd.read_csv('PakNur Bookstore.csv')
with open('./styles.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

def load_lottiefile(file_name: str):
    with open(file_name, 'r') as f:
        return json.load(f)

st.markdown(f"""
    <style>
       .lottie-player {{
            width: 200px;
            height: 200px;
            background: transparent;
        }}
       .lottie-player svg {{
            background: transparent;
        }}
    </style>
""", unsafe_allow_html=True)

lottie_book = load_lottiefile('C6LgbVNJtO.json')
st_lottie(lottie_book, speed=1, height=200, key="initial")

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
    (0.1, 2, 0.2, 1, 0.1)
)

def display_introduction():
    if 'BARANG' in df.columns:
        total_books = df['BARANG'].count()
    else:
        total_books = "Data jumlah buku tidak tersedia"

    total_price = None

    if 'HARGA TOTAL' in df.columns:
        if df['HARGA TOTAL'].isnull().any():
            st.write("There are missing values in the 'HARGA TOTAL' column.")
        else:
            total_price = df['HARGA TOTAL'].sum()
            total_price_rp = f"Rp {total_price:,.2f}"
    else:
        st.write("Data harga total tidak tersedia")
        
    if 'PENERBIT' in df.columns:
        top_seller_publisher = df['PENERBIT'].mode()[0]
    else:
        top_seller_publisher = "Data penerbit tidak tersedia"

    col1, col2, col3 = st.columns((1, 1, 1))

    with col1:
        st.markdown(f"""
            <style>
            .box {{
                    background-color: rgba(0, 0, 0, 0.3);
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 10px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100%;
                }}
            .box h3 {{
                    margin-top: 0;
                    font-size: 24px;  /* Set font size for heading */
                }}
            .box p {{
                    font-size: 20px;  /* Set font size for content */
                }}
            </style>
            <div class="box">
                <h3>Jumlah Buku Terdaftar</h3>
                <p><b>{total_books}</b></p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <style>
            .box {{
                    background-color: rgba(0, 0, 0, 0.3);
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 10px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100%;
                }}
            .box h3 {{
                    margin-top: 0;
                    font-size: 24px;  /* Set font size for heading */
                }}
            .box p {{
                    font-size: 20px;  /* Set font size for content */
                }}
            </style>
            <div class="box">
                <h3>Harga total seluruh Buku</h3>
                <p><b>{total_price_rp}</b></p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <style>
            .box {{
                    background-color: rgba(0, 0, 0, 0.3);
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 10px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100%;
                }}
            .box h3 {{
                    margin-top: 0;
                    font-size: 24px;  /* Set font size for heading */
                }}
            .box p {{
                    font-size: 20px;  /* Set font size for content */
                }}
            </style>
            <div class="box">
                <h3>Top seller buku</h3>
                <p><b>{top_seller_publisher}</b></p>
            </div>
        """, unsafe_allow_html=True)

def scatter_plot_correlation1():
    fig = px.scatter(df, x='HARGA SATUAN', y='PENERBIT')
    st.plotly_chart(fig)

    st.markdown("""
    Dengan visualisasi ini, kita dapat melihat pola hubungan antara 
    harga satuan buku dengan penerbitnya. Jika ada korelasi yang kuat 
    antara harga satuan dengan penerbit, kita akan melihat pola tertentu 
    di mana buku dari penerbit tertentu cenderung memiliki harga satuan 
    tertentu yang lebih tinggi atau lebih rendah daripada penerbit lainnya. 
    Ini bisa memberikan wawasan yang berharga tentang strategi penetapan 
    harga dan preferensi pembelian pelanggan di toko buku Pak Nur.
    """)

def scatter_plot_correlation2():
    fig = px.scatter(df, x='HARGA TOTAL', y='PENERBIT')
    st.plotly_chart(fig)

    st.markdown("""
    Visualisasi scatter plot ini menunjukkan bahwa tidak ada hubungan yang kuat antara 
    penerbit dan harga total bukunya. Hal ini dapat disebabkan oleh beberapa faktor, 
    seperti jenis buku yang diterbitkan, target pasar, dan strategi penetapan harga. 
    Visualisasi ini dapat digunakan untuk mengidentifikasi penerbit yang memiliki 
    harga total buku yang tinggi atau rendah.
    """)

def bar_chart_distribution1():
    fig = px.histogram(df, x='HARGA SATUAN', nbins=5, color_discrete_sequence=['skyblue'])
    fig.update_layout(title='Distribusi Harga Satuan Buku',
                    xaxis_title='Harga Satuan',
                    yaxis_title='Frekuensi',
                    bargap=0.05,
                    bargroupgap=0.1,
                    showlegend=False)

    st.plotly_chart(fig)

    st.markdown("""
    Dari visualisasi bar chart tersebut, terlihat bahwa buku 
    dengan harga di sekitar 40rb memiliki volume penjualan yang cukup tinggi, 
    dan diikuti oleh buku-buku dengan harga berkisar antara 80rb hingga 120rb. 
    Meskipun tidak terlalu signifikan, hal ini menunjukkan bahwa buku dengan harga yang 
    lebih terjangkau, khususnya sekitar 40rb, cenderung lebih diminati daripada buku dengan 
    harga di atas 40rb.
    """)

def bar_chart_distribution2():
    fig = px.histogram(df, x='PENERBIT', nbins=5, color_discrete_sequence=['skyblue'])
    fig.update_layout(title='Distribusi Penerbit Buku',
                    xaxis_title='Penerbit',
                    yaxis_title='Frekuensi',
                    bargap=0.05,
                    bargroupgap=0.1,
                    showlegend=False)

    st.plotly_chart(fig)

    st.markdown("""
    Berdasarkan visualisasi bar chart tersebut, terlihat bahwa Mediatama memiliki frekuensi
    buku paling banyak yaitu 20 buku, lalu diikuti oleh Karya Mandiri Nusantara yang memiliki 
    18 buku. Itu menunjukkan jumlah buku yang terdapat pada toko buku Pak Nur.
    """)

def scatter_plot_relation1():
    fig = px.scatter(df, x='HARGA SATUAN', y='HARGA TOTAL', opacity=0.7)

    fig.update_layout(title='Hubungan Antara Harga Satuan dan Harga Total Buku',
                    xaxis_title='Harga Satuan',
                    yaxis_title='Harga Total')

    st.plotly_chart(fig)
    
    st.markdown("""
    Berdasarkan visualisasi relasi tersebut, terlihat hubungan antara harga satuan 
    dan harga total buku dimana harga total buku selalu lebih tinggi daripada harga satuan buku. 
    Semakin tinggi harga satuan buku, semakin tinggi pula harga total buku. Hal ini 
    menunjukkan bahwa harga satuan buku memiliki hubungan positif dengan harga total buku.
    Hubungan antara harga satuan buku dan harga total buku bersifat linear. Hal ini berarti 
    bahwa setiap kenaikan satu unit harga satuan buku akan diikuti dengan kenaikan harga total 
    buku dengan jumlah yang konstan. Scatter plot tersebut menunjukkan bahwa terdapat 
    hubungan positif dan linear antara harga satuan buku dan harga total buku. Semakin 
    tinggi harga satuan buku, semakin tinggi pula harga total buku.
    """)
    
def scatter_plot_relation2():
    fig = px.scatter(df, x='HARGA SATUAN', y='PENERBIT', opacity=0.7)

    fig.update_layout(title='Hubungan Antara Harga Satuan dan Penerbit',
                    xaxis_title='Harga Satuan',
                    yaxis_title='Penerbit')

    st.plotly_chart(fig)
    
    st.markdown("""
    Dalam visualisasi tersebut, terlihat bahwa rata-rata penerbit memiliki harga buku disekitar
    40rb, hal tersebut menunjukkan hubungan penerbit dengan harga satuan dimana kebanyakan penerbit
    memilih menetapkan harga murah. Meskipun terdapat penerbit yang memiliki harga tertinggi, yaitu
    sekitar 150rb.
    """)

def bar_chart_comparison():
    df_sorted = df.sort_values(by='HARGA SATUAN', ascending=False)

    fig = px.bar(df_sorted, x='PENERBIT', y='HARGA SATUAN', color='PENERBIT')

    fig.update_layout(title='Perbandingan Harga Satuan Berdasarkan Penerbit (Harga Tertinggi)',
                    xaxis_title='Penerbit',
                    yaxis_title='Harga Satuan')

    st.plotly_chart(fig)

    st.markdown("""
    Dari visualisasi tersebut, terlihat bahwa penerbit Lentera Abadi 
    memiliki harga satuan buku tertinggi, mencapai 150rb, diikuti oleh Mediatama dengan harga 102rb
    meski hanya beberapa buku saja, lalu yang ketiga adalah Imperial Bhakti Utama, 
    dengan harga di atas 80rb. Ketiga penerbit 
    tersebut menunjukkan kecenderungan untuk menetapkan harga buku di atas rata-rata, 
    sementara penerbit lainnya cenderung memiliki harga berkisar antara 40rb hingga 50rb.
    """)

def pie_chart():
    fig = px.pie(df, values='BARANG', names='PENERBIT', title='Komposisi Total Barang Berdasarkan Penerbit (Top 2)',
             hole=0.3)

    st.plotly_chart(fig)

    st.markdown("""
    Pada visualisasi pie chart tersebut, terlihat bahwa penerbit 
    Karya Mandiri Nusantara merupakan penerbit terbanyak yaitu sekitar 26% atau sekitar
    35 Buku, diikuti oleh Mediatama dengan 24% kontribusi atau sekitar 33 buku, lalu terdapat
    penerbit Empat Pilar dengan 12 buku atau sekitar 9%.
    """)

def show_cluster():
    pipeline_hc = Pipeline([
        ('scaler', StandardScaler()),
        ('hc', AgglomerativeClustering(n_clusters=4))
    ])

    clusters = pipeline_hc.fit_predict(df[['HARGA SATUAN', 'HARGA TOTAL']])
    df['Cluster'] = clusters

    st.title('Tabel Cluster')

    selected_section = st.selectbox('Pilih Cluster:', ['Scatter Plot Hierarchical', 'Dendrogram Hierarchical'])

    if selected_section == 'Scatter Plot Hierarchical':

        selected_variable = st.selectbox('Pilih Variabel:', ['Kategori Harga', 'Harga Satuan', 'Harga Total'])

        ylabel_mapping = {
            'Kategori Harga': 'HARGA SATUAN',
            'Harga Satuan': 'BARANG',
            'Harga Total': 'HARGA TOTAL'
        }
        y_label = ylabel_mapping[selected_variable]

        xlabel_mapping = {
            'Kategori Harga': 'HARGA TOTAL',
            'Harga Satuan': 'HARGA SATUAN',
            'Harga Total': 'BARANG'
        }
        x_label = xlabel_mapping[selected_variable]

        fig = px.scatter(df, x=x_label, y=y_label, color='Cluster', title='Hierarchical Clustering', 
                        labels={x_label: x_label.capitalize(), y_label: y_label.capitalize()}, 
                        category_orders={'Cluster': sorted(df['Cluster'].unique())})

        st.plotly_chart(fig)

        if selected_variable == 'Kategori Harga':
            st.markdown("""
            Terdapat 4 cluster yang dihasilkan dari pengelompokan data. 
            Cluster pertama terdiri dari data dengan harga satuan dan harga 
            total yang relatif rendah. Sementara itu, cluster kedua terdiri dari 
            data dengan harga satuan yang relatif rendah namun harga total yang relatif 
            tinggi. Di sisi lain, cluster ketiga terdiri dari data dengan harga satuan 
            yang tinggi namun harga total yang rendah. Selanjutnya, cluster keempat 
            terdiri dari data dengan harga satuan dan harga total yang tinggi. 
            Visualisasi hierarchical clustering harga satuan dan harga total 
            membantu memahami pola dan hubungan antar data. Pengelompokan data 
            berdasarkan harga satuan dan harga total dapat memberikan wawasan 
            untuk berbagai analisis, seperti segmentasi pasar, penetapan harga, 
            dan pengambilan keputusan strategis.
            """)
        elif selected_variable == 'Harga Satuan':
            st.markdown("""
            Scatter plot hierarchical clustering tersebut menunjukkan hubungan antara harga satuan dan barang. 
            Dalam plot ini, setiap titik mewakili satu barang, dengan sumbu x menunjukkan 
            harga satuan dan sumbu y menunjukkan jumlah barang.

            Plot ini berguna untuk melihat tren harga barang, membandingkan harga 
            dari kategori yang berbeda, dan mengidentifikasi barang dengan harga 
            tidak biasa. Ini adalah alat yang ampuh untuk visualisasi dan analisis 
            data harga barang, membantu dalam pengambilan keputusan bisnis.
            """)

        elif selected_variable == 'Harga Total':
            st.markdown("""
            Visualisasi tersebut menunjukkan scatter plot hierarchical clustering yang 
            menghubungkan harga total dan jumlah barang. Sumbu X mewakili jumlah barang, 
            sementara sumbu Y menampilkan harga total. Titik-titik data dibagi menjadi 
            beberapa cluster dengan warna yang berbeda.

            Kesimpulannya, harga total cenderung meningkat seiring dengan peningkatan 
            jumlah barang. Pola pembelian konsumen bervariasi, yang mempengaruhi 
            strategi pemasaran dan manajemen inventaris.
            """)
            
    elif selected_section == 'Dendrogram Hierarchical':

        data_pelanggan = pd.read_csv('PakNur Bookstore.csv')
        data_pelanggan_clustering = data_pelanggan[['HARGA SATUAN', 'BARANG', 'HARGA TOTAL']]

        scaler = StandardScaler()
        data_pelanggan_scaled = scaler.fit_transform(data_pelanggan_clustering)

        pca = PCA(n_components=2)
        data_pelanggan_pca = pca.fit_transform(data_pelanggan_scaled)

        linkage_matrix = linkage(data_pelanggan_pca, method='ward')

        dendrogram = ff.create_dendrogram(linkage_matrix)
        dendrogram.update_layout(title='Dendrogram Hierarchical Clustering Pelanggan',
                                xaxis_title='Data Pelanggan',
                                yaxis_title='Jarak Euclidean')

        st.plotly_chart(dendrogram)

    else:
        None

    selected_cluster = st.slider('Pilih Cluster:', 0, df['Cluster'].max(), 0)
    filtered_df = df[df['Cluster'] == selected_cluster]

    st.write(filtered_df)

    st.markdown("""
    Dalam diagram hierachichal clustering tersebut, terdapat empat cluster.
    """)

    st.markdown("---")

    st.subheader('Statistik Cluster')

    cluster_stats = filtered_df.groupby('Cluster').agg(
        Harga_Satuan_Tertinggi=('HARGA SATUAN', 'max'),
        Harga_Satuan_Terendah=('HARGA SATUAN', 'min'),
        Harga_Satuan_Rata_rata=('HARGA SATUAN', 'mean'),
        Harga_Total_Tertinggi=('HARGA TOTAL', 'max'),
        Harga_Total_Terendah=('HARGA TOTAL', 'min'),
        Harga_Total_Rata_rata=('HARGA TOTAL', 'mean'),
    )

    st.write(cluster_stats)

    st.markdown("""
    Dalam tabel tersebut, terlihat masing-masing cluster, dimana setiap cluster
    memiliki kelompok masing-masing, misalkan dalam contoh tersebut, cluster 0,
    yang mana terdapat harga buku satuan tertinggi yaitu 39rb, diikuti dengan
    harga terendah yaitu 30rb, yang dimana rata-rata harga satuan buku sendiri 
    yaitu 30rb. Lalu terdapat pula harga total buku.
    """)

    
def relation_section(relation, selected_columns):
    if relation == "Datasets":
        st.subheader("Dataset")
        if selected_columns:
            filtered_df = df[selected_columns]
            st.dataframe(filtered_df)
        else:
            st.dataframe(df)
    elif relation == "Cluster":
        show_cluster()

def book_summary():
    st.write("Informasi lengkap tentang dataset:")
    st.write(df.info())
    st.write()

    author_publisher_counts = df.groupby(['PENULIS/PENGARANG', 'PENERBIT']).size()
    st.write("Jumlah buku untuk setiap penulis/pengarang dan penerbit:")
    st.write(author_publisher_counts)
    st.write()

    max_price = df['HARGA SATUAN'].max()
    min_price = df['HARGA SATUAN'].min()
    avg_price = df['HARGA SATUAN'].mean()
    oldest_acquisition_date = df['TANGGAL/BULAN/TAHUN PEROLEHAN'].min()

    max_price_str = '{:,.0f}'.format(max_price)
    min_price_str = '{:,.0f}'.format(min_price)
    avg_price_str = '{:,.0f}'.format(avg_price)

    st.write("Buku dengan harga tertinggi:", max_price_str)
    st.write("Buku dengan harga terendah:", min_price_str)
    st.write("Harga rata-rata buku:", avg_price_str)
    st.write()
    st.write("Tahun perolehan buku tertua:", oldest_acquisition_date)

def display_statistik():
    relation_options = ["Korelasi", "Distribusi", "Relasi", "Perbandingan", "Komposisi"]
    selected_relation = st.selectbox("Pilih Visualisasi", relation_options)
    
    correlation_filter = ["Harga Satuan x Penerbit", "Harga Total x Penerbit"]
    distribtuion_filter = ["Frekuensi Harga Satuan", "Frekuensi Penerbit"]

    if selected_relation == "Korelasi":
        selected_filter = st.selectbox("Filter Visualisasi", correlation_filter)
        if selected_filter == "Harga Satuan x Penerbit":
            scatter_plot_correlation1()
        elif selected_filter == "Harga Total x Penerbit":
            scatter_plot_correlation2()
    elif selected_relation == "Distribusi":
        selected_filter = st.selectbox("Filter Visualisasi", distribtuion_filter)
        if selected_filter == "Frekuensi Harga Satuan":
            bar_chart_distribution1()
        elif selected_filter == "Frekuensi Penerbit":
            bar_chart_distribution2()
    elif selected_relation == "Relasi":
        scatter_plot_relation1()
        scatter_plot_relation2()
    elif selected_relation == "Perbandingan":
        bar_chart_comparison()
    elif selected_relation == "Komposisi":
        pie_chart()
    else:
        selected_filter = None

    return selected_relation

def display_data():
    relation_options = ["Datasets", "Cluster"]
    selected_relation = st.selectbox("Pilih Halaman", relation_options)
    
    if selected_relation == "Datasets":
        selected_columns = st.multiselect("Filter", df.columns)
    else:
        selected_columns = None

    return selected_relation, selected_columns
        
def main():
    st.sidebar.image("https://raw.githubusercontent.com/Udinkosd/PakNur-Bookstore-Analysis-App/main/CjAIAxx.png", use_column_width=True) 
    
    st.sidebar.title("Selamat Datang!")

    sections = ["Statistik", "Data"]
    selected_section = st.sidebar.radio("Pilih Halaman", sections)
    
    colors = ["Default", "Water", "Sky", "Gradient"]
    color = st.sidebar.radio("Background", colors)

    color_config = {
        "Default": {"css_class": "stApp", "background_style": ""}, 
        "Water": {"css_class": "stApp", "background_url": "https://images.unsplash.com/photo-1518156677180-95a2893f3e9f?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
        "Sky": {"css_class": "stApp", "background_url": "https://images.unsplash.com/photo-1537420327992-d6e192287183?q=80&w=1976&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
        "Gradient": {"css_class": "stApp", "background_url": "https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=2029&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"}
    }

    css_class = color_config[color]["css_class"]
    background_style = color_config[color].get("background_style", "")
    background_url = color_config[color].get("background_url", "") 

    if background_url:
        st.markdown(f"""
            <style>
             .{css_class} {{
                    background-image: url({background_url});
                    background-size: 50%;
                    background-size: cover;
                }}
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <style>
             .{css_class} {{
                    {background_style}
                }}
            </style>
        """, unsafe_allow_html=True)

    st.title("PakNur Bookstore Analysis App")

    if selected_section == "Statistik":
        display_introduction()
        display_statistik()
        st.write("You are viewing the Statistics section.")
    elif selected_section == "Data":
        selected_relation, selected_columns = display_data()
        relation_section(selected_relation, selected_columns)
        st.write("You are viewing the Data section.")

if __name__ == "__main__":
    main()
