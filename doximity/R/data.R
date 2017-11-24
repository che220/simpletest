library(sqldf)
library(RWeka)
library(data.table)

DATA_DIR = 'C:/apps/doximity'

study = function()
{
    x = loadAllData()
    y=dcast(x, specialty~procedure, value.var='patients')
    y[is.na(y)] = 0
    y$is_card = 'false'
    y$is_card[y$specialty == 'cardiology'] = 'true'
    writeCSV(y, '2.csv')
    
    return (y)
}

## laplace
loadAllData = function()
{
    # verified procedures and their codes are 1-to-1
    proc = loadProcedures()
    totals = aggregate(number_of_patients~physician_id, data=proc, FUN=sum)
    names(totals) = c('physician_id', 'total')
    if (!exists("AGG")) {
        dd = aggregate(number_of_patients~physician_id+procedure_code, data=proc, FUN=sum)
        names(dd)[3] = 'patients'
        AGG <<- dd
    }
    dd = AGG
    
    phys = loadPhysicians()
    specs = data.frame(specialty=sort(unique(phys$specialty)))
    specs$spec_code = paste0('S', seq(1:nrow(specs)))
    specs$spec_code[specs$specialty == 'Cardiology'] = 'Cardiology'
    phys = merge(phys, specs, by='specialty')
    phys = phys[, c('id', 'spec_code')]
    names(phys) = c('physician_id', 'spec_code')
    dd = merge(dd, phys, by='physician_id')
    dd$procedure_code = paste0('P', dd$procedure_code)
    
    y = dcast(dd, physician_id+spec_code~procedure_code, value.var='patients')
    y[is.na(y)] = 0
    
    laplace = 0.1
    y[, 3:ncol(y)] = y[, 3:ncol(y)] + laplace
    y = merge(y, totals, by='physician_id')
    
    cols = names(y)
    codes = cols[grep('^P', cols)]
    for(code in codes) {
        y[[code]] = y[[code]]/(y$total+length(codes)*laplace)
    }
    
    dd = merge(dd, totals, by='physician_id')
    
    dd$norm_patients = dd$patients/dd$total
    
    names(t) = c('specialty', 'physician_count')
    
    names(phys) = c('physician_id', 'specialty')
    dd = merge(proc, phys, by='physician_id')
    
    dd = sqldf("select specialty, procedure_code as procedure, sum(number_of_patients) as patients from dd group by specialty, procedure_code")
    dd$procedure = paste0('P', dd$procedure)
    dd$is_card = 'false'
    dd$is_card[dd$specialty == 'Cardiology'] = 'true'
    
    specs = data.frame(specialty=sort(unique(dd$specialty)))
    specs$spec_code = paste0('S', seq(1:nrow(specs)))
    specs$spec_code[specs$specialty == 'Cardiology'] = 'Cardiology'
    physCnts = merge(t, specs, by='specialty')
    dd = merge(dd, physCnts, by='specialty')
    
    y = dcast(dd, spec_code+physician_count~procedure, value.var='patients')
    y[is.na(y)] = 0
    y[, 3:ncol(y)] = y[, 3:ncol(y)] + 1
    for(i in 3:ncol(y)) {
        print(colnames(y)[i])
        y[, i] = y[,i]/y$physician_count
    }
    
    return (y)
}

loadProcedures = function()
{
    if (!exists("PROCEDURES")) {
        file = file.path(DATA_DIR, 'procedures.csv')
        dd = read.csv(file)
        PROCEDURES <<- dd
    }
    dd = PROCEDURES
    return (dd)
}

loadPhysicians = function()
{
    if (!exists("PHYSICIANS")) {
        file = file.path(DATA_DIR, 'physicians.csv')
        dd = read.csv(file)
        PHYSICIANS <<- dd
    }
    dd = PHYSICIANS
    return (dd)
}

writeCSV = function(df, file, rowNames=FALSE, colNames=TRUE)
{
    options(scipen=500) # turn off scientific notations
    #write.csv(df, file=file, row.names=rowNames, na="", col.names=colNames)
    write.table(df, file=file, row.names=rowNames, col.names=colNames, sep=",")
    print(sprintf("Wrote to %s", file))
}
