def slice_df(df):
    return (lambda df=df: [df.loc[df._loop_status == status, :] for status in ["candidate", "pending", "complete"]])()
