{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "a7557562",
   "metadata": {},
   "source": [
    "# Data Exploration\n",
    "Notes and quick checks for raw data."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "a91d9279",
   "metadata": {},
   "outputs": [],
   "source": [
    "from src.data_preprocessing.load_data import list_audio_files\n",
    "print('files:', list_audio_files('data/raw')[:5])"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
