package com.overwhale.colibri_so.domain.entity;

import lombok.Data;

import javax.persistence.Entity;
import javax.validation.constraints.NotNull;

@Entity
@Data
public class Intent extends BaseEntity {
  
  @NotNull
  private String intent;

  private String description;
}
