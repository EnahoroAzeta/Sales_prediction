{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "fdd543e0",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Run Start: 2021-11-14_23:51:59\n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "from __future__ import print_function\n",
    "import mlflow\n",
    "import time\n",
    "\n",
    "mlflow.set_tracking_uri(\"http://localhost:5000\")\n",
    "mlflow.tracking.get_tracking_uri()\n",
    "def now():\n",
    "    now = int(time.time()+.5)\n",
    "    dt = time.strftime(\"%Y-%m-%d_%H:%M:%S\", time.gmtime(now))\n",
    "    return dt\n",
    "\n",
    "print(\"Run Start:\",now())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "951344bf",
   "metadata": {},
   "outputs": [],
   "source": [
    "experiment_name = \"Sales_Prediction\"\n",
    "Train = pd.read_csv('/Users/apple/Documents/Kaggle/ML_flow_projects/competitive-data-science-predict-future-sales/sales_train.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "8c2c74b7",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "MLflow Version: 1.21.0\n",
      "experiment_id: 3\n",
      "experiment_name: Sales_Prediction\n"
     ]
    }
   ],
   "source": [
    "import mlflow\n",
    "print(\"MLflow Version:\",mlflow.version.VERSION)\n",
    "mlflow.set_experiment(experiment_name)\n",
    "mlflow_client = mlflow.tracking.MlflowClient()\n",
    "experiment_id = mlflow_client.get_experiment_by_name(experiment_name).experiment_id\n",
    "print(\"experiment_id:\",experiment_id)\n",
    "print(\"experiment_name:\",experiment_name)\n",
    "run_origin = \"jupyter\"\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "2a971bd3",
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "import warnings\n",
    "import sys\n",
    "import mlflow.sklearn\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.linear_model import SGDRegressor\n",
    "from sklearn.linear_model import ElasticNet\n",
    "\n",
    "\n",
    "\n",
    "def eval_metrics(actual, pred):\n",
    "    rmse = np.sqrt(mean_squared_error(actual, pred))\n",
    "    mae = mean_absolute_error(actual, pred)\n",
    "    r2 = r2_score(actual, pred)\n",
    "    return rmse, mae, r2"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "09ac92f6",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Training Function\n",
    "\n",
    "    \n",
    "def train(alpha,ll_ratio):\n",
    "\n",
    "    X = Train[['date_block_num','shop_id', 'item_id', 'item_cnt_day']]\n",
    "    y = Train[['item_price']]\n",
    "\n",
    "\n",
    "\n",
    "    # Split the data into training and test sets. (0.75, 0.25) split.\n",
    "    X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.75, test_size=0.2, random_state=0)\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "    with mlflow.start_run() as run:\n",
    "        run_id = run.info.run_uuid\n",
    "        print(\"run_id:\",run_id)\n",
    "        print(\"run_origin:\",run_origin)\n",
    "\n",
    "        global clf\n",
    "        clf = ElasticNet(alpha=alpha, l1_ratio=ll_ratio)\n",
    "\n",
    "\n",
    "        clf.fit(X_train, y_train)\n",
    "\n",
    "        predicted_qualities = clf.predict(X_valid)\n",
    "        (rmse, mae, r2) = eval_metrics(y_valid, predicted_qualities)\n",
    "\n",
    "        print(\"Elasticnet model (alpha={}, ll_ratio={}):\".format(alpha, ll_ratio))\n",
    "        print(\"  RMSE:\",rmse)\n",
    "        print(\"  MAE:\",mae)\n",
    "        print(\"  R2:\",r2)\n",
    "\n",
    "        mlflow.log_param(\"alpha\", alpha)\n",
    "        mlflow.log_param(\"l1_ratio\", ll_ratio)\n",
    "        mlflow.log_param(\"run_origin\", run_origin)\n",
    "        mlflow.log_metric(\"rmse\", rmse)\n",
    "        mlflow.log_metric(\"r2\", r2)\n",
    "        mlflow.log_metric(\"mae\", mae)\n",
    "\n",
    "        mlflow.sklearn.log_model(clf, \"model\")\n",
    "\n",
    "        #X = data.drop([\"quality\"], axis=1).values\n",
    "        #y = data[[\"quality\"]].values.ravel()\n",
    "        #plot_file = \"wine_quality.png\"\n",
    "        #plot_enet_descent_path(X, y, l1_ratio, plot_file)\n",
    "        #mlflow.log_artifact(plot_file)\n",
    "        \n",
    "\n",
    "        return (rmse,r2,mae)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "d5866367",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "run_id: 9ca719753a8a4a35b68997200aa86bfe\n",
      "run_origin: jupyter\n",
      "Elasticnet model (alpha=0.0001, ll_ratio=1):\n",
      "  RMSE: 1697.556286797524\n",
      "  MAE: 724.8474941710072\n",
      "  R2: 0.027875202370595153\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "(1697.556286797524, 0.027875202370595153, 724.8474941710072)"
      ]
     },
     "execution_count": 15,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "train(0.0001,1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "id": "d81cce42",
   "metadata": {},
   "outputs": [],
   "source": [
    "clf\n",
    "import pickle\n",
    "filename = 'sales_prediction_model.pkl'\n",
    "pickle.dump(clf, open(filename, 'wb'))\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f9e7d3c1",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
