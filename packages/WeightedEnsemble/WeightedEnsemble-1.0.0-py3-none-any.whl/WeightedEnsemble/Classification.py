import pandas as pd
import numpy as np
from scipy.optimize import minimize
import os
from sklearn.metrics import *


def Weighted_Ensemble(Models,X_train,y_train,X_val,y_val,X_test,y_test,Method='SLSQP'):
    predictions=0
    pred_prob_val = []
    pred_prob_test=[]
    for i in Models:
        print(str(i) + "started running")
        i.fit(X_train, y_train)
        print(str(i) +' LogLoss {score}'.format(score=log_loss(y_val, i.predict_proba(X_val))))
        pred_prob_val.append(i.predict_proba(X_val))
        pred_prob_test.append(np.round(i.predict_proba(X_test)[:,1],3))
    def log_loss_func(weights):
        final_prediction = 0
        for weight, prediction in zip(weights, pred_prob_val):
                final_prediction += weight*prediction

        return log_loss(y_val, final_prediction)

    starting_values = [0.5]*len(pred_prob_val)

    cons = ({'type':'eq','fun':lambda w: 1-sum(w)})

    bounds = [(0,1)]*len(pred_prob_val)

    res = minimize(log_loss_func, starting_values, method=Method, bounds=bounds, constraints=cons)

    print('Ensamble Score: {best_score}'.format(best_score=res['fun']))
    print('Best Weights: {weights}'.format(weights=res['x']))
    
    for i in range(0,len(pred_prob_test)):
        predictions=predictions+(res['x'][i]*pred_prob_test[i])
    results_test=get_metric_score(y_test, predictions) 
    
    return results_test,res['x']


def get_metric_score(y_true, y_proba):
    best_threshold = 0
    best_score = 0
    accuracy,precision,recall,f1,fpr,thresholds,tnl,fpl,fnl,tpl = [],[],[],[],[],[],[],[],[],[] 
    for threshold in [i * 0.01 for i in range(1,100)]:
            y_pred = (y_proba>threshold).astype(int)
            score=f1_score(y_true=y_true, y_pred=y_pred)
            f1.append(score)
            accuracy.append(accuracy_score(y_true,y_pred))
            precision.append(precision_score(y_true,y_pred))
            recall.append(recall_score(y_true,y_pred))
            tn, fp, fn, tp = confusion_matrix(y_true, y_pred,labels=[0,1]).ravel()
  
            fpr.append(fp/(fp+tn))
            tnl.append(tn)
            fpl.append(fp)
            fnl.append(fn)
            tpl.append(tp)

            thresholds.append(threshold)
            if score > best_score:
                best_threshold = threshold
                best_score = score

    
    model_score_df = pd.DataFrame([thresholds, tpl, fpl, tnl, fnl, accuracy,precision,recall,f1,fpr]).T
    model_score_df.columns = ['threshold', 'tp', 'fp', 'tn', 'fn','accuracy','precision','recall','f1','fpr']
    model_score_df = model_score_df.sort_values(by='threshold',ascending=False)
    model_score_df.loc[:, 'scope'] = (model_score_df['tp']+model_score_df['fp'])/(model_score_df['tp']+model_score_df['fp']+model_score_df['tn']+model_score_df['fn'])
    model_score_df = model_score_df[['threshold', 'tp', 'fp', 'tn', 'fn','accuracy','precision','recall','scope','f1','fpr']]
    search_result = {'threshold': best_threshold, 'f1': best_score}
    return search_result,model_score_df